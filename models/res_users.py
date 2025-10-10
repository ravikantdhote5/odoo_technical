# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    emp_department_id = fields.Many2one(
        'emp.department',
        string="Department",
        required=False,
        readonly=False,
    )
