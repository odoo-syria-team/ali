from odoo import models,api, fields,_



class HeroSection(models.Model):
    _name = 'hero.section.elmakan'
    _description = "this module is for hero.section"

    title=fields.Html(string='Title',required = True)
    image = fields.Binary(string='Image')
    image_url = fields.Char("image url", compute='_compute_image_url')

    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print('base_url' , base_url)
        for obj in self:
            if obj.image:
                print("base_url + '/web/image?' + 'model=images.fanoos&id=' + str(obj.id) + '&field=image'" , base_url + '/web/image?' + 'model=images.fanoos&id=' + str(obj.id) + '&field=image')
                obj.image_url= base_url + '/web/image?' + 'model=images.fanoos&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''