# -*- coding: utf-8 -*-
from odoo import models, fields

class HMSLabTest(models.Model):
    _name = 'hms.lab.test'
    _description = 'Laboratory Test'

    name = fields.Char(string='Test Name', required=True)
    category_id = fields.Many2one('product.category', string='Category')
    product_id = fields.Many2one('product.product', string='Service Product', required=True, 
                                 help='Linked service product for billing')
    price = fields.Float(string='Price', related='product_id.list_price', readonly=True)
    description = fields.Text(string='Description / Instructions')
