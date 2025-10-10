# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Department(models.Model):
    _name = 'emp.department'
    _description = 'Department Model'

    name = fields.Char(string='Department Name', required=True)
    employee_ids = fields.One2many('emp.employee', 'emp_department_id', string="Employees")
    hod_id = fields.Many2one('emp.employee', string='Head of Department')
    hod_user_id = fields.Many2one('res.users', string='HOD User', compute='_compute_hod_user_id', store=True)

    @api.depends('hod_id.user_id')
    def _compute_hod_user_id(self):
        for dept in self:
            dept.hod_user_id = dept.hod_id.user_id
