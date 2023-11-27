
from odoo import models,api, fields,_
from datetime import datetime

class CRMLead(models.Model):
    _inherit = 'crm.lead'  #model name which is going to inherit..

    @api.model
    def create(self, vals): 
        result = super(CRMLead, self).create(vals)
        todos = {   
        'res_id': result.id,    
        'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'crm.lead')]).id,
        'user_id': 2,
        'summary': 'New opportunity added ',
        'note': '',
        'activity_type_id': 4,
        'date_deadline': datetime.today(),
        }   

        data=self.env['mail.activity'].sudo().create(todos)
        return result 