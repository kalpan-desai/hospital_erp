from odoo import models, fields

class PharmacyShelf(models.Model):
    _name = 'pharmacy.shelf'
    _description = 'Pharmacy Shelf'

    name = fields.Char(string='Shelf Location', required=True)
    product_ids = fields.One2many('product.template', 'shelf_id', string='Medicines')
