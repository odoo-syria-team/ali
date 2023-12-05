from odoo import models,api, fields,_


class SaleOrderNiki(models.Model):
    _inherit = 'sale.order'




    def get_vendor_products(self,user_id):
        data =self.env['sale.order'].search([('partner_id' , '=' , user_id.id)])
        records = self.env['output.vendor'].search([])

        # Delete all records
        records.unlink()
        for rec in data:
            for i in rec.order_line:
                self.env['output.vendor'].create({
                'user_id': rec.partner_id.id,
                'product_id': i.product_id.id,
                'product_price': i.price_unit,
                'product_quantity' : i.product_uom_qty
                })