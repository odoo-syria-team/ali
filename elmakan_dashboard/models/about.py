

from odoo import models,api, fields,_



class AboutAlmakaan(models.Model):
    _name = 'about.elmakan'
    _description = "this module is for hero.section"

    text=fields.Html(string='Text',required = True)
    video = fields.Binary(string='Video')