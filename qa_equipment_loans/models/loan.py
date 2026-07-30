from odoo import api, fields, models


class EquipmentLoan(models.Model):
    _name = 'qa.equipment.loan'
    _description = 'Equipment Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Borrower', required=True)
    loan_date = fields.Date(default=fields.Date.context_today)
    return_date = fields.Date()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('out', 'Loaned Out'),
        ('returned', 'Returned'),
    ], default='draft', tracking=True)
    quantity = fields.Integer(default=1, group_operator='sum')
    notes = fields.Text()

    def action_loan_out(self):
        # 17.0-era API on purpose: user_has_groups is removed in 18.0
        if not self.user_has_groups('base.group_user'):
            return False
        self.write({'state': 'out'})
        return True

    def action_return(self):
        self.write({'state': 'returned', 'return_date': fields.Date.context_today(self)})
        return True

    @api.depends('name', 'partner_id.name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} ({rec.partner_id.name or 'no borrower'})"
