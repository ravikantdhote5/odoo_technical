# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_invoice_line_ids = fields.One2many(
        'account.move.custom.line', 'invoice_id', string='Custom Invoice Lines'
    )


class AccountMoveCustomLine(models.Model):
    _name = 'account.move.custom.line'
    _description = 'Custom Invoice Line'

    invoice_id = fields.Many2one('account.move', string='Invoice', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product')
    product_uom_qty = fields.Float(string='Quantity')
    price_unit = fields.Float(string='Unit Price')
    tax_id = fields.Many2many('account.tax', string='Taxes')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.product_uom_qty * line.price_unit


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_order_line_ids = fields.One2many(
        'sale.order.line.custom', 'order_id', string='Custom Order Lines'
    )

    def action_open_custom_line_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manage Custom Lines',
            'res_model': 'custom.order.line.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': self.id
            }
        }

    def _create_invoices(self, grouped, final):
        invoices = super()._create_invoices(grouped=grouped, final=final)

        for order in self:
            for invoice in invoices:
                invoice.custom_invoice_line_ids = [(0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'tax_id': [(6, 0, line.tax_id.ids)] if line.tax_id else [],
                    'subtotal': line.product_uom_qty * line.price_unit,
                }) for line in order.custom_order_line_ids]

        return invoices

    def action_sync_order_lines(self):
        for order in self:
            if not order.order_line:
                raise UserError("No data to sync. Kindly add order lines before syncing.")
            lines_data = []
            for line in order.order_line:
                lines_data.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'name': line.name,
                }))
            order.custom_order_line_ids = lines_data
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Order lines successfully synced to custom order lines.',
                'type': 'success',
                'sticky': False,
            }
        }


    def action_open_custom_order_lines_wizard(self):
        self.ensure_one()
        if not self.custom_order_line_ids:
            raise UserError("No custom order lines found. Please sync or add order lines before opening the wizard.")
        return {
            'name': 'Custom Order Lines',
            'type': 'ir.actions.act_window',
            'res_model': 'custom.order.line.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('employee_management_system.view_custom_order_line_wizard_form').id,
            'target': 'new',
            'context': {'active_id': self.id},
        }


    def action_open_product_list(self):
        self.ensure_one()  # Ensure single record

        # Prepare product lines for QWeb
        products = []
        for line in self.order_line:
            if line.product_id:  # Skip lines with no product
                products.append({
                    'product_id': (line.product_id.id, line.product_id.name),
                    'product_uom_qty': line.product_uom_qty or 0,
                })

        # Render the QWeb template
        html = self.env['ir.qweb']._render(
            'employee_management_system.product_list_template',
            {'products': products}
        )

        return html


class SaleOrderLineCustom(models.Model):
    _name = 'sale.order.line.custom'
    _description = 'Custom Sale Order Line'

    order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    name = fields.Text(string='Description')
    product_uom_qty = fields.Float(string='Quantity', required=True)
    price_unit = fields.Float(string='Unit Price', required=True)
    tax_id = fields.Many2many('account.tax', string='Taxes')

