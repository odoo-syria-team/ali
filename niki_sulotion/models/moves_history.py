from odoo import models,api, fields,_


class StockPicking(models.Model):
    _inherit = 'stock.move'
    _description = "this module is for stock.picking"

    price= fields.Float('Price' , compute = 'get_product_price_from_source', store=True)

    @api.depends('product_id')
    def get_product_price_from_source(self):
        for rec in self:
            if rec.picking_id:
                if rec.picking_id.origin.startswith("P"):
                    po = self.env['purchase.order'].search([('name' , '=' , rec.picking_id.name)])
                    pol = self.env['purchase.order.line'].search([('id' , '=' , po.id),('product_id' , '=' , rec.product_id.name)])
                    rec.price = pol.price_subtotal
                    
                elif rec.picking_id.origin.startswith("S"):
                    po = self.env['sale.order'].search([('name' , '=' , rec.picking_id.name)])
                    pol = self.env['sale.order.line'].search([('id' , '=' , po.id),('product_id' , '=' , rec.product_id.name)])
                    rec.price = pol.price_subtotal
                else:
                    rec.price = 0
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = "this module is for stock.picking"


    partner_id = fields.Many2one('res.partner' , string = 'Partner' , coumpute = 'get_customer' , store=True)
    product_price_ids = fields.Many2many('niki.store.price')

    # @api.constrains('move_ids_without_package')
    # def add_product_price_ids(self):
    #     for rec in self:
            
    #         rec.product_price_ids.unlink()
    #         for line in rec.move_ids_without_package:
    #             self.env['niki.store.price'].create({
    #                 'product_id' :line.product_id.id ,
    #                 'price':line.subtotal
    #             })

    #         rec.product_price_ids += records_to_add
    
    @api.depends('origin')
    def get_customer(self):
        for rec in self:
            if rec.origin:
                if rec.origin.startswith("P"):
                    po = self.env['purchase.order'].search([('name' , '=' , rec.origin)])
                    rec.partner_id = po.partner_id
                elif rec.origin.startswith("S"):
                    so = self.env['sale.order'].search([('name' , '=' , rec.origin)])
                    rec.partner_id = so.partner_id
                else:
                    pass
       
class StorePriceLine(models.Model):
    _name = 'niki.store.price'
    _description = "this module is for niki.store.price"


    product_id =fields.Many2one('product.product')
    price = fields.Float('price')


    def name_get(self):
        result = []
        for rec in self:
            # name = record.points_id.name or ''
            result.append((rec.product_id.name, '%s : %s' % (rec.price)))

        return result




