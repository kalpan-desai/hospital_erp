from odoo import models, fields


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Patient'

    partner_id = fields.Many2one(
        'res.partner',
        string='Patient',
        required=True,
        ondelete='cascade'
    )

    patient_code = fields.Char(string='Patient ID', required=True, copy=False)
    age = fields.Integer(string='Age')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender'
    )
    blood_group = fields.Selection(
        [
            ('a+', 'A+'), ('a-', 'A-'),
            ('b+', 'B+'), ('b-', 'B-'),
            ('ab+', 'AB+'), ('ab-', 'AB-'),
            ('o+', 'O+'), ('o-', 'O-'),
        ],
        string='Blood Group'
    )
    admitted_date = fields.Date(string='Admitted Date')
    is_insured = fields.Boolean(string='Insured')
    note = fields.Text(string='Medical Notes')