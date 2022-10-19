from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Command(models.Model):
    _name = 'qzhub_bot.command'

    command = fields.Char(string="Command", required=True)
    chatbot = fields.Many2one(string='Chatbot', comodel_name="qzhub_bot.bot", required=True, ondelete='cascade')
    model = fields.Many2one(comodel_name="ir.model", string='Chatbot module model')
    filters = fields.Text(string="filters")
    jinja2_template = fields.Text(string="Jinja2 template for answer", required=True)

    @api.onchange('chatbot')
    def set_domain_for_model(self):
        models_name = []
        for rec in self:
            all_models = rec.env['ir.model'].search([])
            for model in all_models:
                model_modules = [module.strip() for module in model.modules.split(",")]
                if rec.chatbot.module.name in model_modules:
                    models_name.append(model.model)
        models_name = tuple(models_name)
        search = self.env['ir.model'].search([('model', 'in', models_name)]).ids
        res = {}
        res['domain'] = {'model': [('id', 'in', search)]}
        return res

    @api.model
    def create(self, vals):
        if vals.get('command'):
            vals['command'] = vals['command'].lower()
        res = super(Command, self).create(vals)
        return res

    def write(self, vals):
        if vals.get('command'):
            vals['command'] = vals['command'].lower()
        res = super(Command, self).write(vals)
        return res

    @api.constrains('command')
    def validate(self):
        for rec in self:
            if len(self.env['qzhub_bot.command'].search([('command', '=', rec.command)])) > 1:
                raise ValidationError(_('Command must be unique'))
