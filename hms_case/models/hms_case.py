# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HMSCase(models.Model):
    _name = 'hms.case'
    _description = 'Patient Case Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'

    name = fields.Char(string='Case Number', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, tracking=True)
    doctor_id = fields.Many2one('res.users', string='Assigned Doctor', tracking=True)
    nurse_ids = fields.Many2many('res.users', string='Assigned Nurses')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('active', 'Active'),
        ('discharged', 'Discharged'),
        ('closed', 'Closed'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    admission_type = fields.Selection([
        ('walk_in', 'Walk-in'),
        ('admission', 'Admission')
    ], string='Admission Type', default='walk_in', tracking=True)
    
    
    start_date = fields.Datetime(string='Start Date', default=fields.Datetime.now)
    end_date = fields.Datetime(string='End Date')
    
    service_line_ids = fields.One2many('hms.case.service', 'case_id', string='Services / Charges')
    vital_ids = fields.One2many('hms.patient.vital', 'case_id', string='Vitals')
    
    move_id = fields.Many2one('account.move', string='Consolidated Invoice', readonly=True)
    total_cost = fields.Monetary(string='Total Cost', compute='_compute_total_cost', store=True, tracking=True)
    currency_id = fields.Many2one('res.currency', related='move_id.currency_id', depends=['move_id.currency_id'])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hms.case') or _('New')
        return super(HMSCase, self).create(vals_list)

    @api.depends('service_line_ids.price_subtotal')
    def _compute_total_cost(self):
        for case in self:
            case.total_cost = sum(line.price_subtotal for line in case.service_line_ids)

    def action_open(self):
        for rec in self:
            rec.state = 'open'

    def action_active(self):
        for rec in self:
            rec.state = 'active'
            
    def action_discharge(self):
        for rec in self:
            rec.state = 'discharged'
            
    def action_close(self):
        for rec in self:
            rec.state = 'closed'
            
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_create_invoice(self):
        self.ensure_one()
        invoice_lines = self._get_invoice_lines()
        
        if not invoice_lines:
            raise UserError(_("There are no services or items to invoice."))
            
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.patient_id.partner_id.id if self.patient_id.partner_id else False,
            'invoice_line_ids': invoice_lines,
            'ref': self.name,
        }
        
        move = self.env['account.move'].create(invoice_vals)
        self.write({'move_id': move.id})
        self._mark_invoiced()
            
        return {
            'name': _('Invoice'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': move.id,
            'type': 'ir.actions.act_window',
        }

    def _get_invoice_lines(self):
        lines = []
        for line in self.service_line_ids.filtered(lambda l: not l.invoiced):
            lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.description or line.product_id.name,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
            }))
        return lines

    def _mark_invoiced(self):
        self.service_line_ids.filtered(lambda l: not l.invoiced).write({'invoiced': True})

    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': self.move_id.id,
            'view_mode': 'form',
        }


class HMSCaseService(models.Model):
    _name = 'hms.case.service'
    _description = 'Case Service Line'

    case_id = fields.Many2one('hms.case', string='Case', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Service/Product', required=True)
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    price_unit = fields.Float(string='Unit Price', required=True)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    invoiced = fields.Boolean(string='Invoiced', default=False, readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.lst_price
            self.description = self.product_id.name

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for record in self:
            record.price_subtotal = record.quantity * record.price_unit
