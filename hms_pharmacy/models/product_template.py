from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_medicine = fields.Boolean(string='Is Medicine', default=False)
    shelf_id = fields.Many2one('pharmacy.shelf', string='Shelf Location')
