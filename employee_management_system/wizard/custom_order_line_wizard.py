# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CustomOrderLineWizard(models.TransientModel):
    _name = 'custom.order.line.wizard'
    _description = 'Wizard: Manage Custom Order Lines'

    order_id = fields.Many2one('sale.order', string="Sale Order")
    wizard_line_ids = fields.One2many('custom.order.line.wizard.line', 'wizard_id', string="Wizard Lines")

    def action_move_to_custom_lines(self):
        for line in self.wizard_line_ids:
            self.env['sale.order.line.custom'].create({
                'order_id': self.order_id.id,
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'tax_id': [(6, 0, line.tax_id.ids)],
            })
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def default_get(self, fields):
        res = super(CustomOrderLineWizard, self).default_get(fields)
        order_id = self.env.context.get('active_id')
        if order_id:
            sale_order = self.env['sale.order'].browse(order_id)
            wizard_lines = []
            for line in sale_order.order_line:
                wizard_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'tax_id': [(6, 0, line.tax_id.ids)],
                }))
            res.update({
                'order_id': order_id,
                'wizard_line_ids': wizard_lines,
            })
        return res


class CustomOrderLineWizardLine(models.TransientModel):
    _name = 'custom.order.line.wizard.line'
    _description = 'Wizard Line: Temporary Order Line'

    wizard_id = fields.Many2one('custom.order.line.wizard', string='Wizard')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    name = fields.Char(string='Description')
    product_uom_qty = fields.Float(string='Quantity', required=True)
    price_unit = fields.Float(string='Unit Price', required=True)
    tax_id = fields.Many2many('account.tax', string='Taxes')
