# -*- coding: utf-8 -*-
from odoo import models, fields


class employee_feedback(models.Model):
    _name = 'employee.feedback'
    _description = 'Feedback'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    comments = fields.Text(string='Comments', required=True)
