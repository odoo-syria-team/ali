

from odoo import models,api, fields,_



class AboutAlmakaan(models.Model):
    _name = 'about.elmakan'
    _description = "this module is for about elmakan"
    _rec_name ='text'
    text=fields.Text(string='Text',required = True,default='')
    video = fields.Text(string='Video',default='')

    content_ids = fields.One2many('about.content.elmakan' , 'about_id' , string= 'Content')
    hero_ids = fields.One2many('about.hero.section.elmakan' , 'about_id' , string= 'Heros')
    gallery_ids = fields.One2many('about.gallery.elmakan' , 'about_id' , string= 'Gallery')
    state = fields.Boolean(string='On WebSite',default=False)
class AboutContentAlmakaan(models.Model): 
    _name ='about.content.elmakan'

    about_id = fields.Many2one('about.elmakan')
    image = fields.Binary(string='Image')
    image_url = fields.Char("image url", compute='_compute_image_url')
    text = fields.Text(string='Text',default='')
    title = fields.Char(string='title',default='')
    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=about.content.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''
   
class AboutHeroAlmakaan(models.Model):
    _name ='about.hero.section.elmakan' 

    about_id = fields.Many2one('about.elmakan')
    image = fields.Binary(string='Image')
    image_url = fields.Char("image url", compute='_compute_image_url')
    text = fields.Html(string='Text',default='')
    title = fields.Char(string='title',default='')

    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=about.hero.section.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''

class AboutGalleryAlmakaan(models.Model):
    _name ='about.gallery.elmakan'   

    about_id = fields.Many2one('about.elmakan') 
    image = fields.Binary(string='Image')
    image_url = fields.Char("image url", compute='_compute_image_url')
    title = fields.Char(string='title',default='')

    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=about.gallery.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''


    