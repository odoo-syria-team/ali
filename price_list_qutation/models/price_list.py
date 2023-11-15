from odoo import models,api, fields,_



class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'
    _description = "this module is for product.pricelist"
    partner_id = fields.Many2one('res.partner' , string = 'Partner' ,required=True)
    def create_quotation(self):
        selected_items = self.env['product.pricelist.item'].search([('pricelist_id', '=', self.id), ('to_select', '!=', False)])
        
        if selected_items:
            quotation_vals = {
                'partner_id': self.partner_id.id,  # Set the partner for the new quotation
                # Add more fields as needed
            }
            
            quotation = self.env['sale.order'].create(quotation_vals)
            
            for item in selected_items:
                # Create the quotation line based on the product.pricelist.item data
                line_vals = {
                    'order_id': quotation.id,
                    'product_id': item.product_id.id,
                    'price_unit': item.fixed_price,
                    # Add more fields as needed
                }
                
                self.env['sale.order.line'].create(line_vals)
            
            # Do any additional operations or actions needed
            # e.g., open the created quotation or show a success message
        else:
            # Handle the case when no items are selected
            pass



class ProductPricelistLine(models.Model):
    _inherit = 'product.pricelist.item'
    _description = "this module is for product.pricelist"



    to_select = fields.Boolean(' ')




