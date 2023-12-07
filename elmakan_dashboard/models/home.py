from odoo import models,api, fields,_



class HomeAlmakaan(models.Model):
    _name = 'home.elmakan'
    _description = "this module is for home elmakan"

    # text=fields.Text(string='Text',required = True,default='')
    # video = fields.Text(string='Video',default='')
    about_id=fields.Many2one('about.elmakan',string='About')
    hero_id=fields.Many2one('hero.section.elmakan',string='Hero')
    features_ids = fields.One2many('home.features.elmakan' , 'home_id' , string= 'Features')
    content_ids = fields.One2many('home.content.elmakan' , 'home_id' , string= 'Content')
    

class HomeFeaturesAlmakaan(models.Model):
    _name = 'home.features.elmakan'
    _description = "this module is for home features elmakan"

    home_id = fields.Many2one('home.elmakan')
    title = fields.Char(string='title',default='')
    link = fields.Char(string='link',default='')
    slug = fields.Char(string='slug',default='')
    image = fields.Binary(string='Image')
    image_url = fields.Char("image url", compute='_compute_image_url')
    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=home.features.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''

class HomeContentAlmakaan(models.Model):
    _name = 'home.content.elmakan'
    _description = "this module is for home content elmakan"

    home_id = fields.Many2one('home.elmakan')
    title = fields.Char(string='title',default='')
    text = fields.Char(string='text',default='')
    link = fields.Char(string='link',default='')
    