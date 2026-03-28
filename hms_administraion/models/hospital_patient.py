from odoo import models, fields, api, _


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

    patient_code = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    dob = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('patient_code', _('New')) == _('New'):
                vals['patient_code'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(HospitalPatient, self).create(vals_list)

    @api.depends('dob')
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.dob:
                rec.age = today.year - rec.dob.year - ((today.month, today.day) < (rec.dob.month, rec.dob.day))
            else:
                rec.age = 0
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