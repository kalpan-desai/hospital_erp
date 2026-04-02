from odoo import models, fields

class DiseaseMaster(models.Model):
    _name = 'health.disease.master'
    _description = 'Disease Master Configuration'

    name = fields.Char(string='Disease Name', required=True)
    impact_score = fields.Float(string='Impact Score', required=True, default=0.0, 
                                help='Penalty points off health score per occurrence')
    severity_factor = fields.Float(string='Severity Factor', required=True, default=1.0,
                                   help='Multiplier applied to the impact score')
