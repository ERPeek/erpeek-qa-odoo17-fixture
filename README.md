# ERPeek QA fixtures: Odoo modules for Migration Pipeline E2E

- `main`: one deliberately 17.0-flavored module (`qa_equipment_loans`) for the 17.0 to 18.0 port.
- `18.0`: one 18.0 module (`qa_service_requests`) for the 18.0 to 19.0 test. It uses patterns
  that change in 19.0 on purpose (`_sql_constraints`, `res.users.groups_id`, `odoo.osv.expression`,
  `read_group`). Not a real product module.
