from odoo import models, fields, api

class HMSCaseInherit(models.Model):
    _inherit = 'hms.case'

    disease_ids = fields.Many2many('health.disease.master', string='Diagnosed Diseases')

class HMSLabTestInherit(models.Model):
    _inherit = 'hms.lab.test'

    normal_min = fields.Float(string='Normal Min Range')
    normal_max = fields.Float(string='Normal Max Range')

class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    medication_type = fields.Selection([
        ('chronic', 'Chronic'),
        ('temporary', 'Temporary'),
        ('none', 'None')
    ], string='Medication Type', default='none')

class HospitalPatientInherit(models.Model):
    _inherit = 'hospital.patient'

    health_score_id = fields.Many2one('health.score', string='Latest Health Score', readonly=True)
    health_category = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('critical', 'Critical')
    ], string='Health Category', related='health_score_id.health_category', store=True)

    def action_view_health_score(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("hms_health_score.action_health_score")
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {'default_patient_id': self.id}
        return action
