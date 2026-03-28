# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HMSLabOrder(models.Model):
    _name = 'hms.lab.order'
    _description = 'Laboratory Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, tracking=True)
    doctor_id = fields.Many2one('res.users', string='Prescribing Doctor', tracking=True)
    
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Urgent'),
        ('2', 'Emergency')
    ], string='Priority', default='0', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    date = fields.Datetime(string='Order Date', default=fields.Datetime.now, tracking=True)
    line_ids = fields.One2many('hms.lab.order.line', 'order_id', string='Tests')
    notes = fields.Text(string='Internal Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hms.lab.order') or _('New')
        records = super(HMSLabOrder, self).create(vals_list)
        records._add_followers()
        return records

    def write(self, vals):
        res = super(HMSLabOrder, self).write(vals)
        if 'patient_id' in vals or 'doctor_id' in vals:
            self._add_followers()
        return res

    def _add_followers(self):
        """ Automatically add patient and doctor as followers """
        for record in self:
            partner_ids = []
            if record.patient_id and record.patient_id.partner_id:
                partner_ids.append(record.patient_id.partner_id.id)
            if record.doctor_id and record.doctor_id.partner_id:
                partner_ids.append(record.doctor_id.partner_id.id)
            
            if partner_ids:
                record.message_subscribe(partner_ids=partner_ids)

    def action_confirm(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_done(self):
        for rec in self:
            rec.state = 'completed'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class HMSLabOrderLine(models.Model):
    _name = 'hms.lab.order.line'
    _description = 'Laboratory Order Line'

    order_id = fields.Many2one('hms.lab.order', string='Order Reference', required=True, ondelete='cascade')
    test_id = fields.Many2one('hms.lab.test', string='Test', required=True)
    price = fields.Float(string='Price', related='test_id.price', readonly=True)
    instructions = fields.Char(string='Instructions')
