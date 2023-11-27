

from odoo import models,api, fields,_



class AboutAlmakaan(models.Model):
    _name = 'about.elmakan'
    _description = "this module is for hero.section"

    text=fields.Text(string='Text',required = True)
    video = fields.Char(string='Video')