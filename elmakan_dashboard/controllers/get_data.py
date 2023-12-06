from odoo import models, fields, api
import json                                  
from odoo import http                           
from odoo.http import request,Response          
import requests    


class Partners(http.Controller):
    # @http.route('/data/brands', auth="public",csrf=False, website=True, methods=['GET'])
    # def get_all_brands(self,**kw): 
    #     result=[]
    #     headers = request.httprequest.headers 

    #     if 'Accept-Language' in headers and headers["Accept-Language"] == "ar":
    #         language = "ar"
    #     else:
    #         language = 'en'
    #     brands = request.env['brand.elmakan'].sudo().search([])
    #     if brands:    
    #         try:
            
                
    #             check_image=lambda image:image if image else ''
    #             for item in brands:
    #                 result.append({
    #                     'id':item.id,
    #                     'title':item.title,              
    #                     'image':check_image(item.image_url),
                        
    #                 })
            
            
            
    #             response = json.dumps({"data":result,'message' : 'All Brands'}) 
    #             return Response(
    #                 response, status=200,
    #                 headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
    #         except Exception as e:
    #             response = json.dumps({'data':[],'message':str(e)}) 
    #             return Response(
    #                 response, status=500,
    #                 headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
    #     else:
    #         if language=='en':
    #             message=''
    #         else:
    #             message=""
    #         response = json.dumps({"data":[],'message':message}) 
    #         return Response(
    #             response, status=400,
    #             headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])

    # @http.route('/data/brands/<int:brand_id>', auth="public",csrf=False, website=True, methods=['GET'])
    # def get_brand_by_id(self,brand_id=None): 
    #     result=[]
    #     headers = request.httprequest.headers

    #     if 'Accept-Language' in headers and headers["Accept-Language"] == "ar":
    #         language = "ar"
    #     else:
    #         language = 'en'
    #     if brand_id:
    #         categories = request.env['brand.elmakan'].sudo().search([('id','=',brand_id)])
    #         if categories:    
    #             try:
                
                    
    #                 check_image=lambda image:image if image else ''
    #                 for item in categories:
    #                     content_obj = request.env['content.brand.elmakan'].sudo().search([('content_id' , '=' ,item.id)])
    #                     gallery_obj = request.env['gallery.brand.elmakan'].sudo().search([('gallery_id' , '=' ,item.id)])
    #                     description_obj = request.env['description.brand.elmakan'].sudo().search([('description_id' , '=' ,item.id)])
    #                     result.append({
    #                         'id':item.id,    
    #                         'title':item.title,              
    #                         'image':check_image(item.image_url),
    #                         'content':[{'id':content.id,'text':content.text,'title':content.title,'image_url':content.image_url} for content in content_obj],
    #                         'gallery':[{'id':gallery.id,'text':gallery.text,'image_url':gallery.image_url} for gallery in gallery_obj],
    #                         'description':[{'id':description.id,'text':description.text,'description':description.description,'title':description.title} for description in description_obj],
                            
                            
    #                     })
                
                
                
    #                 response = json.dumps({"data":result,'message' : 'All categories'}) 
    #                 return Response(
    #                     response, status=200,
    #                     headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
    #             except Exception as e:
    #                 response = json.dumps({'data':[],'message':str(e)}) 
    #                 return Response(
    #                     response, status=500,
    #                     headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
    #         else:
    #             if language=='en':
    #                 message=''
    #             else:
    #                 message=""
    #             response = json.dumps({"data":[],'message':message}) 
    #             return Response(
    #                 response, status=400,
    #                 headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]) 
    #     else:
    #         if language=='en':
    #             message=''
    #         else:
    #             message=""
    #         response = json.dumps({"data":[],'message':message}) 
    #         return Response(
    #             response, status=400,
    #             headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])

    # @http.route('/data/categories', auth="public",csrf=False, website=True, methods=['GET'])
    # def get_all_categories(self,**kw): 
    #     result=[]
    #     headers = request.httprequest.headers
    #     if 'Accept-Language' in headers and headers["Accept-Language"] == "ar":
    #         language = "ar"
    #     else:
    #         language = 'en'
    #     categories = request.env['category.elmakan'].sudo().search([])
    #     if categories:    
    #         try:
            
                
    #             check_image=lambda image:image if image else ''
    #             for item in categories:
    #                 result.append({
    #                     'id':item.id,
    #                     'text':item.text,    
    #                     'title':item.title,              
    #                     'image_url':check_image(item.image_ids.image_url),
                        
    #                 })
            
            
            
    #             response = json.dumps({"data":result,'message' : 'All categyre'}) 
    #             return Response(
    #                 response, status=200,
    #                 headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
    #         except Exception as e:
    #             response = json.dumps({'data':[],'message':str(e)}) 
    #             return Response(
    #                 response, status=500,
    #                 headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
    #     else:
    #         if language=='en':
    #             message=''
    #         else:
    #             message=""
    #         response = json.dumps({"data":[],'message':message}) 
    #         return Response(
    #             response, status=400,
    #             headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])


    @http.route('/data/categories/<int:category_id>', auth="public",csrf=False, website=True, methods=['GET'])
    def get_category_by_id(self,category_id=None): 
        result=[]
        headers = request.httprequest.headers


        if 'Accept-Language' in headers and headers["Accept-Language"] == "ar":
            language = "ar"
        else:
            language = 'en'
        if category_id:
            categories = request.env['category.elmakan'].sudo().search([('id','=',category_id)])
            if categories:    
                try:
                
                    
                    check_image=lambda image:image if image else ''
                    for item in categories:
                        content_obj = request.env['category.content.elmakan'].sudo().search([('category_id' , '=' ,item.id)])
                        gallery_obj = request.env['category.gallery.elmakan'].sudo().search([('category_id' , '=' ,item.id)])
                        boxes_obj = request.env['category.boxes.elmakan'].sudo().search([('category_id' , '=' ,item.id)])
                        result.append({
                            'id':item.id,
                            'text':item.text,    
                            'title':item.title,              
                            'image_url':check_image(item.image_ids.image_url),
                            'content':[{'id':content.id,'text':content.text,'title':content.title,'image_url':content.image_url} for content in content_obj],
                            'gallery':[{'id':gallery.id,'text':gallery.text,'image_url':gallery.image_url} for gallery in gallery_obj],
                            'boxes':[{'id':boxes.id,'text':boxes.text,'title':boxes.title} for boxes in boxes_obj],
                            
                            
                        })
                
                
                
                    response = json.dumps({"data":result,'message' : 'All categories'}) 
                    return Response(
                        response, status=200,
                        headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
                except Exception as e:
                    response = json.dumps({'data':[],'message':str(e)}) 
                    return Response(
                        response, status=500,
                        headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
            else:
                if language=='en':
                    message=''
                else:
                    message=""
                response = json.dumps({"data":[],'message':message}) 
                return Response(
                    response, status=400,
                    headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]) 
        else:
            if language=='en':
                message=''
            else:
                message=""
            response = json.dumps({"data":[],'message':message}) 
            return Response(
                response, status=400,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])


    @http.route('/data/partners', auth="public",csrf=False, website=True, methods=['GET'])
    def get_all_partners(self):
        result=[]
        headers = request.httprequest.headers 
        try:
            partner_obj=request.env['res.partner'].sudo().search([])
            if partner_obj:
                #get_title=lambda x:x.containt_ar if language=='ar' else x.containt_en
                #date=lambda x:str(x) if x!=False else "0000-00-00"
                check_image=lambda image:image if image else ''
                for item in partner_obj:
                    result.append({
                        'id':item.id,
                        'name':item.name                
                    })
            
            
            
            response = json.dumps({"data":result,'message' : 'All partners'}) 
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
        except Exception as e:
            response = json.dumps({'data':[],'message':str(e)}) 
            return Response(
                response, status=500,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])


    @http.route('/data/contact', auth="public",csrf=False, website=True, methods=['GET'])
    def get_all_contact(self):
        result=[]
        headers = request.httprequest.headers 
        try:
            contact_obj=request.env['contact.elmakan'].sudo().search([])
            if contact_obj:
                check_image=lambda image:image if image else ''
                for item in contact_obj:
                    result.append({
                        'id':item.id,
                        'title':item.title,
                        'text':item.text,
                        'link':item.link ,
                        'icon':item.image_url,
                    })
            
            
            
            response = json.dumps({"data":result,'message' : 'All contact'}) 
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
        except Exception as e:
            response = json.dumps({'data':[],'message':str(e)}) 
            return Response(
                response, status=500,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
        
    @http.route('/data/hero_section', auth="public",csrf=False, website=True, methods=['GET'])
    def get_hero_section(self):
        result=[]
        headers = request.httprequest.headers 
        try:
            partner_obj=request.env['hero.section.elmakan'].sudo().search([],limit=1)
            if partner_obj:
                #get_title=lambda x:x.containt_ar if language=='ar' else x.containt_en
                #date=lambda x:str(x) if x!=False else "0000-00-00"
                check_image=lambda image:image if image else ''
                for item in partner_obj:
                    result.append({
                        'id':item.id,
                        'title':item.title,
                        'image_url':item.image_url                
                    })
            
            
            
            response = json.dumps({"data":result,'message' : 'Hero Section'}) 
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
        except Exception as e:
            response = json.dumps({'data':[],'message':str(e)}) 
            return Response(
                response, status=500,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])

    # @http.route('/data/aboutUS', auth="public",csrf=False, website=True, methods=['GET'])
    # def get_aboutUS(self):
    #     result=[]
    #     headers = request.httprequest.headers 
    #     try:
    #         partner_obj=request.env['about.elmakan'].sudo().search([],limit=1)
    #         if partner_obj:
    #             #get_title=lambda x:x.containt_ar if language=='ar' else x.containt_en
    #             #date=lambda x:str(x) if x!=False else "0000-00-00"
    #             check_str=lambda x:x if x else ''
    #             check_image=lambda image:image if image else ''
    #             for item in partner_obj:
    #                 result.append({
    #                     'id':item.id,
    #                     'text':check_str(item.text),
    #                     'video':check_str(item.video)                
    #                 })
            
            
    #         if result:
    #             result=result[0]
    #         else:
    #             result={}
    #         response = json.dumps({"data":result,'message' : 'About US'}) 
    #         return Response(
    #             response, status=200,
    #             headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])
    #     except Exception as e:
    #         response = json.dumps({'data':[],'message':str(e)}) 
    #         return Response(
    #             response, status=500,
    #             headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])

    @http.route('/Brand', auth="public",csrf=False, website=True, methods=['GET'])
    def get_all_brands(self): 
        result=[]
        headers = request.httprequest.headers
        try:
            brand_obj=request.env['brand.elmakan'].sudo().search([])
            slider_obj=request.env['brand.slider.elmakan'].sudo().search([])
            check_list=lambda x:x[0] if x else {} 
            check_str=lambda x:x if x else ""
            result=[
                {
                    'brandSlider': [
                        {
                            'title': check_str(slider.title),
                            'image': check_str(slider.image_url)
                        }
                        for slider in slider_obj],
                    'brands': [
                        {
                            'title': check_str(brand.title),
                            'slug': check_str(brand.slug),
                            'image': check_str(brand.image_url),
                            
                        }
                        for brand in brand_obj]    
                }
            ]
           
            if result:
                result=result[0]
            else:
                result={}    
            response = json.dumps({"brands":result,'message' : 'All Brands'}) 
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])    

        except Exception as e:
            response = json.dumps({'data':{},'message':str(e)}) 
            return Response(
                response, status=500,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])

    @http.route('/BrandBySlug/<string:slug>', auth="public",csrf=False, website=True, methods=['GET'])
    def get_BrandBySlug(self,slug): 
        result=[]
        headers = request.httprequest.headers
        try:
            brand_obj=request.env['brand.elmakan'].sudo().search([('slug','=',slug)])
            check_list=lambda x:x[0] if x else {} 
            check_str=lambda x:x if x else ""
            for item in brand_obj:
                result.append({
                    'image': check_str(item.image_url),
                    'title': check_str(item.title),
                    'content': [
                            {
                            'title': check_str(content.title),
                            'image': check_str(content.image_url),
                            'text': check_str(content.text)
                            }
                        for content in item.content_ids],
                    'description': check_list([{
                            'title': check_str(des.title),
                            'description-text': check_str(des.description),
                            'text': check_str(des.text)
                        } for des in item.description_ids]),  
                    "gallery": [
                            {
                            "image": gallery.image_url,
                            "text": gallery.text
                            }
                        for gallery in item.gallery_ids]      
                })
                
            response = json.dumps({"brand":result,'message' : 'Brand Details'}) 
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])    

        except Exception as e:
            response = json.dumps({'data':{},'message':str(e)}) 
            return Response(
                response, status=500,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])


    @http.route('/Gatergories', auth="public",csrf=False, website=True, methods=['GET'])
    def get_all_Gatergories(self): 
        result=[]
        headers = request.httprequest.headers
        try:
            category_obj=request.env['category.elmakan'].sudo().search([])
            check_list=lambda x:x[0] if x else {} 
            check_str=lambda x:x if x else ""
            for item in category_obj:
                result.append({
                    'image': check_str(item.image_url),
                    'title': check_str(item.title),
                    'text': check_str(item.text),
                    'slug': check_str(item.slug)
                })
                
            response = json.dumps({"categories":result,'message' : 'All Categories'}) 
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])    

        except Exception as e:
            response = json.dumps({'data':{},'message':str(e)}) 
            return Response(
                response, status=500,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])                


    @http.route('/CategoriesBySlug/<string:slug>', auth="public",csrf=False, website=True, methods=['GET'])
    def get_CategoriesBySlug(self,slug): 
        result=[]
        headers = request.httprequest.headers
        try:
            category_obj=request.env['category.elmakan'].sudo().search([('slug','=',slug)])
            check_list=lambda x:x[0] if x else {} 
            check_str=lambda x:x if x else ""
            for item in category_obj:
                result.append({
                    'title': check_str(item.title),
                    'image': check_str(item.image_url),
                    'text': check_str(item.text),
                    'content': [
                            {
                            'title': check_str(content.title),
                            'image': check_str(content.image_url),
                            'text': check_str(content.text)
                            }
                        for content in item.content_ids], 
                    "gallery": [
                            {
                            "image": gallery.image_url,
                            "text": gallery.text
                            }
                        for gallery in item.gallery_ids],   
                    'boxes': [{ 'title': box.title, 'text': box.text } for box in item.boxes_ids]        
                })
                
            response = json.dumps({"Categories":result,'message' : 'Category Details'}) 
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])    

        except Exception as e:
            response = json.dumps({'data':{},'message':str(e)}) 
            return Response(
                response, status=500,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])


    @http.route('/About', auth="public",csrf=False, website=True, methods=['GET'])
    def get_About(self): 
        result=[]
        headers = request.httprequest.headers
        try:
            about_obj=request.env['about.elmakan'].sudo().search([],limit=1)
            check_list=lambda x:x[0] if x else {} 
            check_str=lambda x:x if x else ""
            for item in about_obj:
                result.append({
                    'text':check_str(item.text),
                    'video':check_str(item.video),
                    "hero": [
                        {
                            'image':check_str(hero.image_url),
                            'title':check_str(hero.title),
                            'text': check_str(hero.text)
                        }
                        for hero in item.hero_ids],
                    'content': [
                            {
                            'image': check_str(content.image_url),
                            'title': check_str(content.title),
                            'text': check_str(content.text)
                            }
                        for content in item.content_ids], 
                    "gallery": [
                            {
                            "image": gallery.image_url,
                            "title": gallery.title
                            }
                        for gallery in item.gallery_ids],   
                        
                })
            if result:
                result=result[0]
            else:
                result={}    
            response = json.dumps({"aboutUs":result,'message' : 'AboutUs Details'}) 
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])    

        except Exception as e:
            response = json.dumps({'data':{},'message':str(e)}) 
            return Response(
                response, status=500,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)]) 


    @http.route('/Home', auth="public",csrf=False, website=True, methods=['GET'])
    def get_Home(self): 
        result=[]
        headers = request.httprequest.headers
        try:
            home_obj=request.env['home.elmakan'].sudo().search([],limit=1)
            check_list=lambda x:x[0] if x else {} 
            check_str=lambda x:x if x else ""
            for item in home_obj:
                result.append({
                    "hero": check_list([{
                        "title": check_str(hero.title),
                        "image": check_str(hero.image_url)
                    } for hero in item.hero_id]),
                    "about": check_list([{
                        "text": check_str(about.text),
                        "video": check_str(about.video)
                    } for about in item.about_id]),
                    "features": [
                        {
                        "title": check_str(feature.title),
                        "link":check_str(feature.link),
                        "image": check_str(feature.image_url),
                        "slug": check_str(feature.slug)
                        }
                    for feature in item.features_ids],
                    "contact-boxes": [
                        {
                        "title": check_str(content.title),
                        "text": check_str(content.text),
                        "link": check_str(content.link)
                        }
                    for content in item.content_ids]
                    
                        
                })
            if result:
                result=result[0]
            else:
                result={}    
            response = json.dumps({"Home":result,'message' : 'Home Details'}) 
            return Response(
                response, status=200,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])    

        except Exception as e:
            response = json.dumps({'data':{},'message':str(e)}) 
            return Response(
                response, status=500,
                headers=[('Content-Type', 'application/json'), ('Content-Length', 100)])                        