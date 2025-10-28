# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError,ValidationError
from datetime import date
import logging


_logger = logging.getLogger(__name__)
class Employee(models.Model):
    _name = 'emp.employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Model'
    _rec_name = 'full_name'

    first_name = fields.Char(string='First Name', required='True', tracking=True)
    last_name = fields.Char(string='Last Name', required='True', tracking=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    email = fields.Char(string='Email',required='True', tracking=True)
    phone = fields.Char(string='Phone',required='True', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth',required='True')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender',required='True', tracking=True)
    address = fields.Text(string='Address',required='True', tracking=True)
    hire_date = fields.Date(string='Hire Date',required='True', tracking=True)
    salary = fields.Float(string='Salary', tracking=True)
    user_id = fields.Many2one('res.users', string='Assigned Admin', tracking=True)
    emp_department_id = fields.Many2one(
        'emp.department',
        string="Department",
        required=False,
        readonly=False,
        tracking=True
    )
    has_skills = fields.Boolean(string='Has Skills', compute='_compute_has_skills')
    hod_name = fields.Char(string='Head of Department', related='emp_department_id.hod_id.full_name', store=True)
    color = fields.Char('Color', default='#FFFFFF')

    is_favourite = fields.Boolean(string="Favourite")
    is_toggle = fields.Boolean(string="Toggle")

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'Email must be unique!'),
        ('positive_age', 'CHECK(age >= 0)', 'Age must be positive!'),
    ]
    status = fields.Selection([
        ('intern', 'Intern'),
        ('junior', 'Junior'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
        ('manager', 'Manager'),
    ], string='Status', default='intern')

    skill_ids = fields.Many2many(
        'emp.skill',
        'emp_employee_skill_rel',
        'employee_id',
        'skill_id',
        string='Skills'
    )

    priority = fields.Selection([
        ('1', '★☆☆☆☆'),
        ('2', '★★☆☆☆'),
        ('3', '★★★☆☆'),
        ('4', '★★★★☆'),
        ('5', '★★★★★'),
        ('6', '★★★★★★'),
    ], string='Priority', default='1')

    @api.depends('skill_ids')
    def _compute_has_skills(self):
        for rec in self:
            rec.has_skills = bool(rec.skill_ids)

    @api.depends('employee_ids.department_id')
    def _compute_department_id(self):
        for user in self:
            if user.employee_ids:
                user.department_id = user.employee_ids[0].department_id.id
            else:
                user.department_id = False

    @api.depends('department_id')
    def _compute_hod_name(self):
        for rec in self:
            if rec.department_id and rec.department_id.hod_id:
                rec.hod_name = rec.department_id.hod_id.full_name
            else:
                rec.hod_name = ''

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                dob = record.date_of_birth
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                record.age = age
            else:
                record.age = 0

    @api.onchange('hire_date')
    def _onchange_hire_date(self):
        if self.hire_date and self.hire_date < fields.Date.to_date('2025-01-01'):
            return {
                'warning': {
                    'title': "Invalid Hire Date",
                    'message': "Hire Date cannot be before January 1, 2025.",
                }
            }

    @api.constrains('phone', 'email')
    def _check_phone_and_email(self):
        for record in self:
            if record.phone and (not record.phone.isdigit() or len(record.phone) != 10):
                raise ValidationError("Phone number must be exactly 10 digits.")
            if record.email and '@' not in record.email:
                raise ValidationError("Email must contain '@' symbol.")

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = (record.first_name or '') + ' ' + (record.last_name or '')

    def action_promote(self):
        promotion_order = ['intern', 'junior', 'senior', 'lead', 'manager']
        for record in self:
            current_index = promotion_order.index(record.status)
            if current_index < len(promotion_order) - 1:
                record.status = promotion_order[current_index + 1]
                if record.status == 'manager':
                    raise UserError(_("Now you are the Manager"))
            else:
                raise UserError(_("Promotion not possible. Already at highest status."))

    def action_view_skills(self,*args):
        self.ensure_one()
        if not self.skill_ids:
            raise UserError("This employee has no skills to display.")
        return {
            'name': 'Skills',
            'type': 'ir.actions.act_window',
            'res_model': 'emp.skill',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.skill_ids.ids)],
            'target': 'current',
            'context': {
            'edit': False,
            'create': False,
            'delete': False,
        },
        }

    def create_record(self):
        print("Create Records")

        context = dict(self.env.context or {})
        context['default_address'] = 'Indore'

        emp_model = self.env['emp.employee'].with_context(context)
        defaults = emp_model.default_get(['address'])
        default_address = defaults.get('address', '')

        vals = {
            'first_name': self.first_name or '',
            'last_name': self.last_name or '',
            'phone':'',
            'date_of_birth': self.date_of_birth or '',
            'gender': self.gender or '',
            'address':default_address,
            'hire_date': fields.Date.context_today(self),
            'salary': 5000.0,
        }
        rec = self.env['emp.employee'].create(vals)
        print((f"Record: {rec.first_name} {rec.last_name} ({rec.id},)"))
        return rec

    def update(self):
        print("Update Records")
        employee_ids = self.env['emp.employee'].search([('first_name', '=', 'Ravi')]).ids
        employees = self.env['emp.employee'].browse(employee_ids)
        employees.write({'last_name': 'Sharma'})

    def search_method(self):
        print("Search Records")
        employee = self.env['emp.employee'].browse([1, 2, 3])
        employee2 = self.env['emp.employee'].search([('first_name','=','Ravi')])
        employee3 = self.env['emp.employee'].search_count([('first_name', '=', 'Ravi')])
        employee4 = self.env['emp.employee'].search_read([('first_name', '=', 'Ravi')], fields=['first_name', 'last_name'], limit=3)
        employee5 = self.env['emp.employee'].name_search('Ravi', limit=3)
        employee6 = self.env['emp.employee'].read_group(
            domain=[('gender', '=', 'male')],
            fields=['salary:sum', 'address'],
            groupby=['address']
        )
        employees = self.env['emp.employee'].search([])
        employees1 = employees.filtered(lambda e: e.first_name == 'Ravi')

        print("Employee:", employee)
        print("Employee:", employee2)
        print("Employee:", employee3)
        print("Employee:", employee4)
        print("Employee:", employee5)
        print("Employee:", employee6)
        print("Employee:", employees1)

    def delete_method(self):
        print("Deleting employee records with first_name = 'John'...")
        employees = self.env['emp.employee'].search([('first_name', '=', 'John')])

        if employees:
            count = len(employees)
            employees.unlink()
            print(f"Deleted {count} employee record(s).")
        else:
            print("No employee records found to delete.")

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record.message_post(
            body="A new record has been created.",
            message_type='notification',
            subtype_xmlid='mail.mt_note'
        )
        return record

    def write(self, vals):
        res = super().write(vals)
        self.message_post(
            body="The record has been updated.",
            message_type='notification',
            subtype_xmlid='mail.mt_note'
        )
        return res

    def button_log_message(self):
        self.message_post(body="Custom log message from button click")

    @api.model
    def send_birthday_wishes(self):
        today = fields.Date.context_today(self)
        employees = self.search([('date_of_birth', '=', today)])
        if not employees:
            _logger.info("No employees with birthday today.")
        for emp in employees:
            _logger.info(f"Sending birthday wishes to {emp.name}")
