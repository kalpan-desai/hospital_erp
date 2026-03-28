# -*- coding: utf-8 -*-
from odoo import models, fields

class HMSPatientVital(models.Model):
    _name = 'hms.patient.vital'
    _description = 'Patient Vital Sign'
    _order = 'date desc'

    case_id = fields.Many2one('hms.case', string='Case', required=True, ondelete='cascade')
    patient_id = fields.Many2one('hospital.patient', related='case_id.patient_id', string='Patient', store=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now, required=True)
    
    vital_type = fields.Selection([
        ('bp', 'Blood Pressure (mmHg)'),
        ('hr', 'Heart Rate (bpm)'),
        ('temp', 'Temperature (°C/°F)'),
        ('rr', 'Respiratory Rate (breaths/min)'),
        ('spo2', 'SpO2 (%)'),
        ('weight', 'Weight (kg)'),
        ('height', 'Height (cm)'),
        ('other', 'Other')
    ], string='Vital Type', required=True)
    
    value = fields.Char(string='Value', required=True)
    notes = fields.Text(string='Notes')
