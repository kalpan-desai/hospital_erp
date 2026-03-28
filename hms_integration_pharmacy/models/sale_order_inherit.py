from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    case_id = fields.Many2one('hms.case', string='Linked Case', tracking=True)
