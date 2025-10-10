# -*- coding: utf-8 -*-
from odoo import models, fields


class Skill(models.Model):
    _name = 'emp.skill'
    _description = 'Employee Skill'

    name = fields.Char(string='Skill Name', required=True)
    description = fields.Text(string='Description')
    employee_ids = fields.Many2many(
        'emp.employee',
        'emp_employee_skill_rel',
        'skill_id',
        'employee_id',
        string='Employees'
    )
