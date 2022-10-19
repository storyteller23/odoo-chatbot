from odoo import models, fields, api

class ChatBot(models.Model):
    _name = 'qzhub_bot.bot'

    name = fields.Char(string="Bot name", required=True)
    module = fields.Many2one(string='Module',
                                  comodel_name="ir.module.module",
                                  required=True,
                                  ondelete='cascade',
                                  domain=[('state', '=', 'installed')])

    @api.depends("module")
    def _compute_inherit_models(self):
        inherit_models = []
        for rec in self:
            all_models = rec.env['ir.model'].search([])
            for model in all_models:
                model_modules = [module.strip() for module in model.modules.split(",")]
                if rec.module.name in model_modules:
                    if model_modules[0] != rec.module.name:
                        inherit_models.append(model.model)
        search_inherit = self.env['ir.model'].search([('model', 'in', inherit_models)]).ids
        print(tuple(search_inherit))
        for rec in self:
            rec.inherit_models = False
            rec.inherit_models = [(6, 0, tuple(search_inherit))]

    @api.depends("module")
    def _compute_native_models(self):
        native_models = []
        for rec in self:
            all_models = rec.env['ir.model'].search([])
            for model in all_models:
                model_modules = [module.strip() for module in model.modules.split(",")]
                if rec.module.name in model_modules:
                    if model_modules[0] == rec.module.name:
                        native_models.append(model.model)
        search_native = self.env['ir.model'].search([('model', 'in', native_models)]).ids
        print(tuple(search_native))
        for rec in self:
            rec.native_models = False
            rec.native_models = [(6, 0, tuple(search_native))]


    native_models = fields.Many2many(string='Native models', comodel_name='ir.model', relation="ir_model_chat_bot_rel", compute="_compute_native_models")
    inherit_models = fields.Many2many(string='Inherit models', comodel_name='ir.model', relation="ir_model_chat_bot_rel", compute="_compute_inherit_models")
    command_ids = fields.One2many("qzhub_bot.command", "chatbot", string="Commands")
    is_active = fields.Boolean(string="Is active", default=True)

    # @api.onchange('module')
    # def set_domain_for_model(self):
    #     native_models = []
    #     inherit_models = []
    #     for rec in self:
    #         all_models = rec.env['ir.model'].search([])
    #         for model in all_models:
    #             model_modules = [module.strip() for module in model.modules.split(",")]
    #             if rec.module.name in model_modules:
    #                 if model_modules[0] == rec.module.name:
    #                     native_models.append(model.model)
    #                 else:
    #                     inherit_models.append(model.model)
    #     native_models = tuple(native_models)
    #
    #     inherit_models = tuple(inherit_models)
    #     search_native = self.env['ir.model'].search([('model', 'in', native_models)]).ids
    #     search_inherit = self.env['ir.model'].search([('model', 'in', inherit_models)]).ids
    #     res = {}
    #     res['domain'] = {
    #                      'native_models': [('id', 'in', search_native)],
    #                      'inherit_models': [('id', 'in', search_inherit)],
    #                      }
    #     return res
