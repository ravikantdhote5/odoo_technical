# -*- coding: utf-8 -*-
from odoo import fields, models, api

# class ProductProduct(models.Model):
#     _inherit = 'product.product'
#
#     pos_description = fields.Char(string="POS Description",
#                                   help="Custom description visible in POS.")
#
#     @api.model
#     def create(self, vals):
#         product = super(ProductProduct, self).create(vals)
#         if 'pos_description' in vals and product.product_tmpl_id:
#             product.product_tmpl_id.pos_description = vals['pos_description']
#         return product
#
#     def write(self, vals):
#         if 'pos_description' in vals:
#             for product in self:
#                 if product.product_tmpl_id:
#                     product.product_tmpl_id.pos_description = vals['pos_description']
#         return super(ProductProduct, self).write(vals)
#
#
# class ProductTemplate(models.Model):
#     _inherit = 'product.template'
#
#     pos_description = fields.Char(string="POS Description",
#                                   help="Custom description visible in POS.",
#                                   compute='_compute_pos_description', store=True)
#
#     @api.depends('product_variant_ids.pos_description')
#     def _compute_pos_description(self):
#         for template in self:
#             variant_pos_desc = template.product_variant_ids.mapped('pos_description')
#             if variant_pos_desc:
#                 template.pos_description = variant_pos_desc[0]
#             else:
#                 template.pos_description = False


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_description = fields.Char(string="POS Description",
                                  help="Description",
                                  readonly=False
                                  )
    slices_per_pizza = fields.Integer(string="Slices per Pizza",
                                      default=1,
                                      help="Number of slices contained in one pizza")
    slice_you_got = fields.Integer(string="Slices")



class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    pos_description = fields.Char(
        related="product_tmpl_id.pos_description",
        store=True,
    )

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields += ['pos_description']
        return fields
