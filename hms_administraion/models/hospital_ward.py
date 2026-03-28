# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Hospitalward(models.Model):
    _name = 'hospital.ward'
    _description = 'Hospital Ward'
    _order = 'name'

    name = fields.Char(
        string="Ward Name",
        required=True
    )

    code = fields.Char(
        string="Ward Code",
        required=True,
        help="Unique code for the ward"
    )

    ward_type = fields.Selection([
        ('general', 'General'),
        ('icu', 'ICU'),
        ('private', 'Private'),
        ('emergency', 'Emergency'),
        ('maternity', 'Maternity'),
    ], string="Ward Type", required=True, default='general')

    capacity = fields.Integer(
        string="Total Beds",
        required=True
    )

    active = fields.Boolean(
        default=True
    )

    note = fields.Text(
        string="Notes"
    )

    _sql_constraints = [
        ('ward_code_unique', 'unique(code)', 'Ward code must be unique!')
    ]
