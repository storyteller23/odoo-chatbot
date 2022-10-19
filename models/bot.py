from odoo import models, _
import jinja2


class Bot(models.AbstractModel):
    _inherit = 'mail.bot'

    def get_answer_from_template(self, command):
        environment = jinja2.Environment()
        template = environment.from_string(command[0].jinja2_template)
        model_name = command[0].model.model
        if not model_name:
            return template.render()
        filters = command[0].filters
        converted_filters = []
        if filters:
            for line in filters.split('\n'):
                a, op, b = line.strip().split()
                converted_filters.append((a, op, b))
        finded = self.env[model_name].search(converted_filters)
        return template.render(objects=finded)

    def _get_answer(self, record, body, values, command=False):
        command = self.env['qzhub_bot.command'].search([('command', '=', body)])
        if command:
            if command[0].chatbot.is_active:
                return self.get_answer_from_template(command)

        return super()._get_answer(record, body, values, command)
