from odoo import models, fields

class HMSLabOrder(models.Model):
    _inherit = 'hms.lab.order'

    case_id = fields.Many2one('hms.case', string='Linked Case', tracking=True)
