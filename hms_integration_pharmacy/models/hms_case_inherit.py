from odoo import models, fields, api, _

class HMSCase(models.Model):
    _inherit = 'hms.case'

    def _get_invoice_lines(self):
        lines = super(HMSCase, self)._get_invoice_lines()
        
        pharmacy_orders = self.env['sale.order'].search([('case_id', '=', self.id), ('state', 'in', ['sale', 'done'])])
        for order in pharmacy_orders:
            for line in order.order_line:
                if not line.invoice_lines:
                    lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'name': f"Pharmacy: {line.name}",
                        'quantity': line.product_uom_qty,
                        'price_unit': line.price_unit,
                    }))
                
        return lines

    def action_open_pharmacy_orders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Pharmacy Orders'),
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('case_id', '=', self.id)],
            'context': {'default_case_id': self.id, 'default_partner_id': self.patient_id.partner_id.id if self.patient_id.partner_id else False},
        }

    def action_prescribe_medicine(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Prescribe Medicine'),
            'res_model': 'sale.order',
            'view_mode': 'form',
            'context': {'default_case_id': self.id, 'default_partner_id': self.patient_id.partner_id.id if self.patient_id.partner_id else False},
        }
