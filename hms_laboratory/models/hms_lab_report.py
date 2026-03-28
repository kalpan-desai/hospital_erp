# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HMSLabReport(models.Model):
    _name = 'hms.lab.report'
    _description = 'Laboratory Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Report Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    order_id = fields.Many2one('hms.lab.order', string='Lab Order', required=True, tracking=True)
    patient_id = fields.Many2one('hospital.patient', related='order_id.patient_id', string='Patient', store=True)
    doctor_id = fields.Many2one('res.users', related='order_id.doctor_id', string='Doctor', store=True)

    date = fields.Datetime(string='Report Date', default=fields.Datetime.now)
    result = fields.Html(string='Results', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], string='Status', default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hms.lab.report') or _('New')
        records = super(HMSLabReport, self).create(vals_list)
        records._add_followers()
        return records

    def write(self, vals):
        res = super(HMSLabReport, self).write(vals)
        if 'order_id' in vals:
            self._add_followers()
        return res

    def _add_followers(self):
        for record in self:
            partner_ids = []
            if record.patient_id and record.patient_id.partner_id:
                partner_ids.append(record.patient_id.partner_id.id)
            if record.doctor_id and record.doctor_id.partner_id:
                partner_ids.append(record.doctor_id.partner_id.id)
            if partner_ids:
                record.message_subscribe(partner_ids=partner_ids)

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            # Auto send mail
            email_values = {
                'subject': f"Your Lab Report is ready: {rec.name}",
                'body_html': f"""
                    <p>Dear {rec.patient_id.name},</p>
                    <p>Your laboratory report (<b>{rec.name}</b>) is now available.</p>
                    <p>Best regards,<br/>Hospital Laboratory</p>
                """,
            }
            rec.message_post(body=email_values['body_html'], subject=email_values['subject'], message_type='email', subtype_xmlid='mail.mt_comment')
