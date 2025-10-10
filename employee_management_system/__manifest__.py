# -*- coding: utf-8 -*-
{
    'name': 'Employee Management System',
    'version': '1.0',
    'summary': 'Manage Employees and Departments',
    'description': """
        This module allows you to manage employees and their departments,
        including personal and job-related information.
    """,
    'category': 'Human Resources',
    'author': 'Ravikant',
    'website': 'https://yourcompanywebsite.com',
    'depends': ['base', 'hr', 'sale', 'account','mail','web'],
    'data': [
        'security/emp_groups.xml',
        'security/emp_rules.xml',
        'security/ir.model.access.csv',
        'views/actions.xml',
        'views/client_action.xml',
        'views/employee_management_system_menus.xml',
        'views/employee_management_system_views.xml',
        'views/emp_department_views.xml',
        'views/employee_skills_views.xml',
        'views/sale_order_custom_lines.xml',
        'views/account_move_custom_lines.xml',
        'views/basic_template.xml',
        'wizard/custom_order_line_wizard_view.xml',
        'views/res_users_views.xml',
        'data/cron_data.xml',
        'report/report_employee_action.xml',
        'report/report_employee_template.xml',
        'report/report_sale_order.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'employee_management_system/static/src/js/feedback_page.js',
            'employee_management_system/static/src/xml/feedback_page.xml',
            'employee_management_system/static/src/css/feedback_page.css',
            'employee_management_system/static/src/js/global_button_controller.js',
            # 'employee_management_system/static/src/js/control_panel_extension.js',
            # 'employee_management_system/static/src/xml/client_action_template.xml',
            'employee_management_system/static/src/xml/global_button_template.xml',
            # 'employee_management_system/static/src/xml/gl_button.xml',
        ],
    },



    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
