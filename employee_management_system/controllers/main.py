# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class BasicController(http.Controller):
    @http.route("/hello", type="http", auth="public")
    def hello(self):
        return "Hello World!"


class HelloWorldController(http.Controller):
    @http.route('/helloworld', type='http', auth='public', website=True)
    def hello(self, **kwargs):
        name = kwargs.get('name', 'World')
        return request.render('employee_management_system.hello_page', {'name': name})


class HelloWorldAPI(http.Controller):
    @http.route('/api/hellow', type='json', auth='public')
    def api_hello(self, **kwargs):
        name = kwargs.get('name', 'World')
        return {'message': f'Hello, {name}!'}


class MyFormController(http.Controller):
    @http.route('/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def submit(self, **post):
        name = post.get('name', 'Anonymous')
        return f"Submitted name: {name}"


class EmployeeManagementController(http.Controller):

    @http.route('/employee_management/custom_page', type='http', auth='user')
    def custom_page(self, **kwargs):
        return request.render('employee_management_system.custom_employee_page')
