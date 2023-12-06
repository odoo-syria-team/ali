from odoo import models,api, fields,_



class CategoryAlmakaan(models.Model):
    _name = 'category.elmakan'
    _description = "this module is for hero.section"

    text=fields.Text(string='Text')
    image = fields.Binary(string='Image')
    title =fields.Char(string='title')
    content_ids = fields.One2many('category.content.elmakan' , 'category_id' , string= 'Content')
    boxes_ids = fields.One2many('category.boxes.elmakan' , 'category_id' , string= 'Boxes')
    gallery_ids = fields.One2many('category.gallery.elmakan' , 'category_id' , string= 'Gallery')
    image_url = fields.Char("image url", compute='_compute_image_url')
    slug = fields.Char(string='Slug',default='')
    # video= fields.Text(string='video')
    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print('base_url' , base_url)
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=category.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''
class CategoryContentAlmakaan(models.Model):
    _name = 'category.content.elmakan'
    _description = "this module is for category.content.elmakan"


    category_id = fields.Many2one('category.elmakan')
    text=fields.Text(string='Text')
    image = fields.Binary(string='Image')
    title =fields.Char(string='Title')
    image_url = fields.Char("image url", compute='_compute_image_url')

    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print('base_url' , base_url)
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=category.content.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''

class CategoryGalleryAlmakaan(models.Model):
    _name = 'category.gallery.elmakan'
    _description = "this module is for category.gallery.elmakan"


    category_id = fields.Many2one('category.elmakan')
    text=fields.Text(string='Text')
    image = fields.Binary(string='Image')
    image_url = fields.Char("image url", compute='_compute_image_url')

    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print('base_url' , base_url)
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=category.gallery.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''


class CategoryBoxesAlmakaan(models.Model):
    _name = 'category.boxes.elmakan'
    _description = "this module is for category.boxes.elmakan"


    category_id = fields.Many2one('category.elmakan')
    text =fields.Text(string='text')
    title =fields.Char(string='title')
