from odoo import models, fields, api, _

class HMSCase(models.Model):
    _inherit = 'hms.case'

    def _get_invoice_lines(self):
        lines = super(HMSCase, self)._get_invoice_lines()
        
        lab_orders = self.env['hms.lab.order'].search([('case_id', '=', self.id), ('state', '=', 'completed')])
        for order in lab_orders:
            for line in order.line_ids:
                lines.append((0, 0, {
                    'product_id': line.test_id.product_id.id if line.test_id.product_id else False,
                    'name': f"Lab: {line.test_id.name}",
                    'quantity': 1,
                    'price_unit': line.price,
                }))
                
        return lines

    def action_open_lab_orders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Lab Orders'),
            'res_model': 'hms.lab.order',
            'view_mode': 'list,form',
            'domain': [('case_id', '=', self.id)],
            'context': {'default_case_id': self.id, 'default_patient_id': self.patient_id.id},
        }

    def action_request_lab_test(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Request Lab Test'),
            'res_model': 'hms.lab.order',
            'view_mode': 'form',
            'context': {'default_case_id': self.id, 'default_patient_id': self.patient_id.id},
        }
