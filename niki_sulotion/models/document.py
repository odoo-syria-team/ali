from odoo import models,api, fields,_
from datetime import datetime

class DocumentNikki(models.Model):
    _name = 'document.nikki' 
    _rec_name='file_name'

    user_id = fields.Many2one('res.users',string='User' ,default=lambda self: self.env.user.id) 
    category_id = fields.Many2one('category.nikki' , string='Category')
    file_data = fields.Binary('File')
    file_name = fields.Char('File Name')


class CategoryDocument(models.Model):
    _name= 'category.nikki'

    name = fields.Char('Category Name')