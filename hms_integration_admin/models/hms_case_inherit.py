from odoo import models, fields, api

class HMSCase(models.Model):
    _inherit = 'hms.case'

    bed_id = fields.Many2one('hospital.bed', string='Allocated Bed', tracking=True)

    def _get_invoice_lines(self):
        lines = super(HMSCase, self)._get_invoice_lines()
        
        # Add bed charges
        if self.bed_id and self.bed_id.product_id:
            duration = 1
            if self.start_date and self.end_date:
                delta = self.end_date.date() - self.start_date.date()
                duration = max(1, delta.days)
                
            lines.append((0, 0, {
                'product_id': self.bed_id.product_id.id,
                'name': f"Bed Charge: {self.bed_id.name}",
                'quantity': duration,
                'price_unit': self.bed_id.product_id.lst_price,
            }))
            
        return lines

    @api.depends('bed_id', 'start_date', 'end_date')
    def _compute_total_cost(self):
        super(HMSCase, self)._compute_total_cost()
        for case in self:
            if case.bed_id and case.bed_id.product_id:
                duration = 1
                if case.start_date and case.end_date:
                    delta = case.end_date.date() - case.start_date.date()
                    duration = max(1, delta.days)
                case.total_cost += duration * case.bed_id.product_id.lst_price
