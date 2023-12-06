from odoo import models,api, fields,_



class BrandAlmakaan(models.Model):
    _name = 'brand.elmakan'
    _description = "this module is for brand"

    slug = fields.Char(string='Slug',default='')
    image = fields.Binary('Image')
    title = fields.Text('Title')
    description_ids = fields.One2many('description.brand.elmakan' , 'description_id' , string='Description')
    content_ids = fields.One2many('content.brand.elmakan' , 'content_id' , string='Content')
    gallery_ids = fields.One2many('gallery.brand.elmakan' , 'gallery_id' , string='Gallery')
    image_url = fields.Char("image url", compute='_compute_image_url')
    

    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print('base_url' , base_url)
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=brand.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''


class BrandSliderAlmakaan(models.Model):
    _name = 'brand.slider.elmakan'
    _description = "this module is for brand slider elmakan"

    title = fields.Text('Title',default='')
    image = fields.Binary('Image')
    image_url = fields.Char("image url", compute='_compute_image_url')


    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=brand.slider.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''


class DescriptionBrandAlmakaan(models.Model):
    _name = 'description.brand.elmakan'
    _description = "this module is for brand"

    title = fields.Text('Title')
    description = fields.Text('Description')
    text = fields.Text('Text')
    description_id = fields.Many2one('brand.elmakan')

class ContentBrandAlmakaan(models.Model):
    _name = 'content.brand.elmakan'
    _description = "this module is for brand"

    title = fields.Text('Title')
    text = fields.Text('Text')
    content_id = fields.Many2one('brand.elmakan')
    image = fields.Binary('Image')
    image_url = fields.Char("image url", compute='_compute_image_url')


    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print('base_url' , base_url)
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=content.brand.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''

class ContentBrandAlmakaan(models.Model):
    _name = 'gallery.brand.elmakan'
    _description = "this module is for brand"

    text = fields.Text('Text')
    gallery_id = fields.Many2one('brand.elmakan')
    image = fields.Binary('Image')
    image_url = fields.Char("image url", compute='_compute_image_url')


    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print('base_url' , base_url)
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=gallery.brand.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''