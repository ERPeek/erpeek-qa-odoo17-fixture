# Written in Odoo 18.0 syntax on purpose. Several patterns here change in 19.0:
# _sql_constraints (models.Constraint), res.users.groups_id (group_ids),
# odoo.osv.expression (odoo.fields.Domain) and read_group (_read_group).
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class QaServiceRequest(models.Model):
    _name = 'qa.service.request'
    _description = 'Service Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, id desc'

    name = fields.Char(required=True, copy=False, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    sale_order_id = fields.Many2one('sale.order', string='Sales Order')
    user_id = fields.Many2one('res.users', string='Technician', default=lambda self: self.env.user, tracking=True)
    priority = fields.Selection([('0', 'Normal'), ('1', 'High'), ('2', 'Urgent')], default='0')
    state = fields.Selection(
        [('new', 'New'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancel', 'Cancelled')],
        default='new', tracking=True,
    )
    hours = fields.Float(string='Hours Spent')
    hourly_rate = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    amount = fields.Monetary(compute='_compute_amount', store=True, currency_field='currency_id')
    partner_request_count = fields.Integer(compute='_compute_partner_request_count')
    reference = fields.Char(copy=False)

    _sql_constraints = [
        ('reference_unique', 'unique(reference)', 'The reference must be unique.'),
        ('hours_positive', 'CHECK(hours >= 0)', 'Hours cannot be negative.'),
    ]

    @api.depends('hours', 'hourly_rate')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.hours * rec.hourly_rate

    def _compute_partner_request_count(self):
        groups = self.read_group(
            [('partner_id', 'in', self.partner_id.ids)], ['partner_id'], ['partner_id'],
        )
        counts = {g['partner_id'][0]: g['partner_id_count'] for g in groups}
        for rec in self:
            rec.partner_request_count = counts.get(rec.partner_id.id, 0)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('qa.service.request') or _('New')
        return super().create(vals_list)

    def _open_domain(self):
        return expression.AND([
            [('state', 'in', ('new', 'in_progress'))],
            [('user_id', '=', self.env.uid)],
        ])

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        manager = self.env.ref('qa_service_requests.group_service_manager')
        if self.filtered(lambda r: r.hours <= 0) and manager not in self.env.user.groups_id:
            raise UserError(_('Only a service manager can close a request without hours.'))
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})
