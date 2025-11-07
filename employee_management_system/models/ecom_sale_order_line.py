# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):

        result = super()._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)

        line_id = result.get('line_id')
        if not (product_id and line_id):
            return result

        line = self.env['sale.order.line'].browse(line_id)
        product = self.env['product.product'].browse(product_id)
        factor = product.slices_per_pizza or 0.0

        try:
            total_output = float(kwargs.get('slice_you_got', 0.0))
        except (ValueError, TypeError):
            total_output = line.product_uom_qty * factor

        line.write({
            'slices_per_pizza': factor,
            'slice_you_got': total_output or (line.product_uom_qty * factor),
        })
        return result


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    slices_per_pizza = fields.Integer(string="Slices per Pizza",
                                      default=5,
                                      help="Number of slices contained in one pizza")
    slice_you_got = fields.Integer(string="Slices")

    @api.onchange('product_id', 'product_uom_qty', 'slices_per_pizza')
    def _onchange_values(self):
        for line in self:
            if line.product_id:
                line.slices_per_pizza = line.product_id.slices_per_pizza or line.slices_per_pizza
            line.slice_you_got = (line.product_uom_qty or 0.0) * (line.slices_per_pizza or 0.0)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            qty = vals.get('product_uom_qty') or 0.0
            factor = vals.get('slices_per_pizza') or 0.0
            if not vals.get('slice_you_got') and qty and factor:
                vals['slice_you_got'] = qty * factor
        return super().create(vals_list)