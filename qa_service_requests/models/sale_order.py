from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    service_request_ids = fields.One2many('qa.service.request', 'sale_order_id', string='Service Requests')
    service_request_count = fields.Integer(compute='_compute_service_request_count')

    def _compute_service_request_count(self):
        for order in self:
            order.service_request_count = len(order.service_request_ids)

    def action_view_service_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'qa.service.request',
            'view_mode': 'list,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {'default_sale_order_id': self.id, 'default_partner_id': self.partner_id.id},
        }
