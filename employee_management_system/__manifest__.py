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
    'depends': ['base', 'hr', 'sale', 'account','mail','web','website_sale','point_of_sale'],
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
        # 'views/sale_order_custom_lines.xml',
        'views/account_move_custom_lines.xml',
        'views/basic_template.xml',
        'views/sale_order_views.xml',
        'views/pos_geninfo_view.xml',
        'views/pos_product_view.xml',
        # 'views/product_template_view.xml',
        'views/website_product_template.xml',
        # 'views/product_list_template.xml',
        'views/pos_sale_order_line.xml',
        'wizard/custom_order_line_wizard_view.xml',
        'views/res_users_views.xml',
        'data/cron_data.xml',
        'report/report_employee_action.xml',
        'report/report_employee_template.xml',
        'report/report_sale_order.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'employee_management_system/static/src/js/custom_boolean_toggle.js',
            'employee_management_system/static/src/js/employee_rpc.js',
            'employee_management_system/static/src/xml/employee_rpc.xml',
            'employee_management_system/static/src/js/feedback_page.js',
            'employee_management_system/static/src/xml/feedback_page.xml',
            'employee_management_system/static/src/css/feedback_page.css',
            'employee_management_system/static/src/js/feedback_data.js',
            'employee_management_system/static/src/xml/feedback_data.xml',
            'employee_management_system/static/src/js/global_button_controller.js',
            'employee_management_system/static/src/xml/global_button_template.xml',
            'employee_management_system/static/src/js/custom_form_controller.js',
            'employee_management_system/static/src/js/product_list.js',
            'employee_management_system/static/src/xml/product_list.xml',
            # 'employee_management_system/static/src/xml/custom_import.xml',
        ],

        'web.assets_frontend': [
            '/employee_management_system/static/src/js/slices_counter.js',
            # '/employee_management_system/static/src/js/website_slice.js',
        ],

        'point_of_sale._assets_pos': [
            'employee_management_system/static/src/xml/product_information_popup.xml',
]
    },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
