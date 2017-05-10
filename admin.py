#coding:utf-8
import wsgiref.handlers 
import os
from functools import wraps
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models import Images
import methods,logging
import descriptor 

class AdminControl(webapp.RequestHandler):
    def render(self,template_file,template_value):
        path=os.path.join(os.path.dirname(__file__),template_file)
        self.response.out.write(template.render(path, template_value))
    def returnjson(self,dit):
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(simplejson.dumps(dit))

class Admin_Upload(AdminControl):
    def get(self):
        self.render('views/upload.html', {})
    
    def post(self):
        bf=self.request.get("file")
        if not bf:
            return self.redirect('/admin/upload/')
        name=self.request.body_file.vars['file'].filename
        mime = self.request.body_file.vars['file'].headers['content-type']
        if mime.find('image')==-1:
             return self.redirect('/admin/upload/')
         
        description=descriptor.dhash(bf)
        image=methods.addImage( mime, description, bf, name) 
        self.redirect('/show/%s/' %image.id)

class Find(AdminControl):
    def get(self):
        self.render('views/find.html', {})
        
    def post(self):
        bf=self.request.get("file")
        if not bf:
            return self.redirect('/admin/find/')
        name=self.request.body_file.vars['file'].filename
        mime = self.request.body_file.vars['file'].headers['content-type']
        if mime.find('image')==-1:
             return self.redirect('/admin/find/')

        description=descriptor.dhash(bf)
        
        images=Images.all().order('-created_at').fetch(30,0)
        max=-1
        git=None
        for image in images:
            if descriptor.compare_hash(image.description,description) > max:
                max=descriptor.compare_hash(image.description,description)
                gid=image
        
        image=methods.addImage( mime, description, bf, name)      
        template_value={"git":gid,"simil":max,"image":image}
        self.render('views/gausshow.html', template_value)
            
class Delete_Image(AdminControl):

    def get(self,key):
        methods.delImage(key)
        self.redirect('/')
    

    
application = webapp.WSGIApplication(
                                       [(r'/admin/upload/', Admin_Upload),
                                        (r'/admin/find/', Find),
                                        (r'/admin/del/(?P<key>[a-z,A-Z,0-9]+)', Delete_Image),
                                       ], debug=True)
wsgiref.handlers.CGIHandler().run(application)

