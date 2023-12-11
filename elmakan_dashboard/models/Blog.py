from odoo import models,api, fields,_
from odoo.exceptions import ValidationError
from datetime import datetime ,date,timedelta


class BlogElmakan(models.Model):
    _name = 'blog.almakan'
    _description = "this module is for blog "

    image = fields.Image(string='Image')
    image_url= fields.Char(string='Image url',compute='_compute_image_url')
    title = fields.Char(string='Title', default='')
    content =  fields.Html(string='Content',default='')
    slug = fields.Char(string='Slug', default='')
    tag = fields.Char(string='tag', default='')
    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=blog.almakan&id=' + str(obj.id) + '&field=image'
            else :
                obj.image_url= ''


