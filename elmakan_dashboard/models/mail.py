from odoo import models,api, fields,_



class MailAlmakaan(models.Model):
    _name = 'mail.elmakan'
    _description = "this module is for mail elmakan"

    app_key = fields.Char(string='App Key',default='')
    company_email = fields.Char(string='Company Email',default='')