# -*- coding: utf-8 -*-
# © 2018 Sedarome (http://www.sedarome.fr)
# @author Nicolas Farrie <n.farrie@es-natura.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import itertools
import psycopg2

from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError, RedirectWarning, except_orm


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def create_variant_ids(self):
        Product = self.env["product.product"]
        AttributeValues = self.env['product.attribute.value']
        for tmpl_id in self.with_context(active_test=False):
            # adding an attribute with only one value should not recreate product
            # write this attribute on every product to make sure we don't lose them
            variant_alone = tmpl_id.attribute_line_ids.filtered(
                lambda line: line.attribute_id.create_variant and len(line.value_ids) == 1).mapped('value_ids')
            for value_id in variant_alone:
                updated_products = tmpl_id.product_variant_ids.filtered(
                    lambda product: value_id.attribute_id not in product.mapped('attribute_value_ids.attribute_id'))
                updated_products.write({'attribute_value_ids': [(4, value_id.id)]})

            # iterator of n-uple of product.attribute.value *ids*
            variant_matrix = [
                AttributeValues.browse(value_ids)
                for value_ids in itertools.product(*(line.value_ids.ids for line in tmpl_id.attribute_line_ids if
                                                     line.value_ids[:1].attribute_id.create_variant))
            ]

            # get the value (id) sets of existing variants
            existing_variants = {
                frozenset(variant.attribute_value_ids.filtered(lambda r: r.attribute_id.create_variant).ids) for variant
                in tmpl_id.product_variant_ids}
            # -> for each value set, create a recordset of values to create a
            #    variant for if the value set isn't already a variant
            to_create_variants = [
                value_ids
                for value_ids in variant_matrix
                if set(value_ids.ids) not in existing_variants
            ]

            # check product
            variants_to_activate = self.env['product.product']
            variants_to_unlink = self.env['product.product']
            for product_id in tmpl_id.product_variant_ids:
                if not product_id.active and product_id.attribute_value_ids.filtered(
                        lambda r: r.attribute_id.create_variant) in variant_matrix:
                    variants_to_activate |= product_id
                elif product_id.attribute_value_ids.filtered(
                        lambda r: r.attribute_id.create_variant) not in variant_matrix:
                    variants_to_unlink |= product_id
            if variants_to_activate:
                variants_to_activate.write({'active': True})

            # create new product
            # If we want to add new variant , we search about the last variante number
            product_ids = self.env['product.product'].search([('product_tmpl_id', '=', self._ids[0])],
                                                             order='variante_num DESC', limit=1)
            i = product_ids.variante_num if product_ids else 0
            for variant_ids in to_create_variants:
                i += 1
                new_variant = Product.create({
                    'product_tmpl_id': tmpl_id.id,
                    'attribute_value_ids': [(6, 0, variant_ids.ids)],
                    'variante_num': i
                })

            # unlink or inactive product
            for variant in variants_to_unlink:
                try:
                    with self._cr.savepoint(), tools.mute_logger('odoo.sql_db'):
                        variant.unlink()
                # We catch all kind of exception to be sure that the operation doesn't fail.
                except (psycopg2.Error, except_orm):
                    variant.write({'active': False})
                    pass
        return True
