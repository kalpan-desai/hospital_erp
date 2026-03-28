# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HospitalBed(models.Model):
    _name = 'hospital.bed'
    _description = 'Hospital Bed'
    
    name = fields.Char(string='Bed Number', required=True)
    ward_id = fields.Many2one('hospital.ward', string='Ward', required=True, ondelete='cascade')
    state = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance')
    ], string='Status', default='available')
    product_id = fields.Many2one('product.product', string='Bed Charge Service', 
                                 help='Service product used for billing this bed per day')
    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('name_ward_uniq', 'unique (name, ward_id)', 'Bed number must be unique per ward!')
    ]
