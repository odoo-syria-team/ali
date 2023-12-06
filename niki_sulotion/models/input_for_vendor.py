from odoo import models, api, fields, _


class InputVendors(models.Model):
    _name = 'input.vendor'
    _description = ''
    user_id = fields.Many2one('res.partner', string='User Name')
    product_id = fields.Many2one('product.product', string='Product')
    product_price = fields.Float('Price')
    product_quantity = fields.Integer('Quantity')

    def get_vendor_products(self):
        action = self.env['purchase.order'].get_vendor_products()

        return True


class OutputVendors(models.Model):
    _name = 'output.vendor'
    _description = ''
    user_id = fields.Many2one('res.partner', string='User Name')
    product_id = fields.Many2one('product.product', string='Product')
    product_price = fields.Float('Price')
    product_quantity = fields.Integer('Quantity')

    def get_vendor_products(self):
        action = self.env['sale.order'].get_vendor_products()

        return True
