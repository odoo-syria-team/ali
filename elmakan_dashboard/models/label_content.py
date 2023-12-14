from odoo import models,api, fields,_



class LabelContentAlmakaan(models.Model):
    _name = 'labelcontent.elmakan'
    _description = "this module is for label content elmakan"
    _rec_name ='title'
    title = fields.Text(string='Title',default='')
    text = fields.Char(string='Text',default='')

    content_ids = fields.One2many('label.content.elmakan' , 'label_id' , string= 'Content')
    slider_ids = fields.One2many('label.slider.elmakan' , 'label_id' , string= 'Sliders')
    box_ids = fields.One2many('label.box.elmakan' , 'label_id' , string= 'Boxs')
    state = fields.Boolean(string='On WebSite',default=False)

class LContentAlmakaan(models.Model): 
    _name ='label.content.elmakan'

    label_id = fields.Many2one('labelcontent.elmakan')
    image = fields.Binary(string='Image')
    image_url = fields.Char("image url", compute='_compute_image_url')
    text = fields.Text(string='Text',default='')
    title = fields.Text(string='Title',default='')

    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=label.content.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''


class LSliderAlmakaan(models.Model): 
    _name ='label.slider.elmakan'

    label_id = fields.Many2one('labelcontent.elmakan')
    image = fields.Binary(string='Image')
    image_url = fields.Char("image url", compute='_compute_image_url')
    text = fields.Text(string='Text',default='')
    title = fields.Text(string='Title',default='')

    @api.depends('image')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for obj in self:
            if obj.image:
                obj.image_url= base_url + '/web/image?' + 'model=label.slider.elmakan&id=' + str(obj.id) + '&field=image'
            else:
                obj.image_url=''


class LBoxAlmakaan(models.Model): 
    _name ='label.box.elmakan'

    label_id = fields.Many2one('labelcontent.elmakan')
    text = fields.Text(string='Text',default='')
    title = fields.Text(string='Title',default='')
