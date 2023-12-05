from odoo import models,api, fields,_
import re
import os
import time
import base64 
from odoo.exceptions import ValidationError

class InputNiki(models.TransientModel):
    _name = 'input.product.niki'
    _description = " "

    user_id=fields.Many2one('res.partner' ,string='Vendor' ,required = True)
    
    def button_show_tree_view(self):
        self.ensure_one()
        
        self.env['purchase.order'].get_vendor_products(self.user_id)
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Vendor products',
            'view_mode': 'tree',
            'res_model': 'input.vendor',
            'domain': [],  # Optionally define a domain
            'context': dict(self.env.context),
        }
        return action
    
class OutputNiki(models.TransientModel):
    _name = 'output.product.niki'
    _description = " "

    user_id=fields.Many2one('res.partner' ,string='Customer' ,required = True)
    
    def button_show_tree_view(self):
        self.ensure_one()
        
        self.env['sale.order'].get_vendor_products(self.user_id)
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Vendor products',
            'view_mode': 'tree',
            'res_model': 'output.vendor',
            'domain': [],  # Optionally define a domain
            'context': dict(self.env.context),
        }
        return action
    
