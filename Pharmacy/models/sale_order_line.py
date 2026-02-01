from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    med_morning = fields.Float(
        string='Morning',
        help='Number of doses in the morning'
    )
    med_afternoon = fields.Float(
        string='Afternoon',
        help='Number of doses in the afternoon'
    )
    med_evening = fields.Float(
        string='Evening',
        help='Number of doses in the evening'
    )
    med_duration_days = fields.Integer(
        string='Duration (Days)',
        help='Number of days the medicine is to be taken'
    )

    @api.onchange('med_morning', 'med_afternoon', 'med_evening', 'med_duration_days', 'product_id')
    def _onchange_compute_quantity(self):
        """Compute quantity based on schedule and duration for medicines."""
        for line in self:
            if line.product_id and line.product_id.is_medicine and line.med_duration_days:
                doses_per_day = (line.med_morning or 0) + (line.med_afternoon or 0) + (line.med_evening or 0)
                if doses_per_day > 0:
                    line.product_uom_qty = doses_per_day * line.med_duration_days

    def _prepare_invoice_line(self, **optional_values):
        """Copy schedule fields to invoice line."""
        res = super()._prepare_invoice_line(**optional_values)
        res.update({
            'med_morning': self.med_morning,
            'med_afternoon': self.med_afternoon,
            'med_evening': self.med_evening,
            'med_duration_days': self.med_duration_days,
        })
        return res

