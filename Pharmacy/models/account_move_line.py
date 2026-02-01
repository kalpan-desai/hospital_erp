from odoo import models, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    med_morning = fields.Float(string='Morning')
    med_afternoon = fields.Float(string='Afternoon')
    med_evening = fields.Float(string='Evening')
    med_duration_days = fields.Integer(string='Duration (Days)')
