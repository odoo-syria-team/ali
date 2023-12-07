from odoo import models, api, fields, _


class PurchaseOrderNiki(models.Model):
    _inherit = 'purchase.order'

    def get_vendor_products(self, user_id):
        data = self.env['purchase.order'].search([('partner_id', '=', user_id.id)])
        records = self.env['input.vendor'].search([])

        # Delete all records
        records.unlink()
        for rec in data:
            for i in rec.order_line:
                self.env['input.vendor'].create({
                    'user_id': rec.partner_id.id,
                    'po' : rec.id,
                    'product_id': i.product_id.id,
                    'product_price': i.price_unit,
                    'product_quantity': i.product_qty
                })
