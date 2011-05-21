#!/usr/bin/env python

from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms

import cgi
import os
import string
import logging
import random

from django import forms


class Link(db.Model):
	url = db.LinkProperty(required=True)
	category = db.CategoryProperty(required=True)
	
	
class LinkForm(djangoforms.ModelForm):
	
	error_css_class = 'error'
	required_css_class = 'required'
	
	url = forms.URLField(
		max_length=200,
		required=True,
		label="URL",
		help_text="The URL.",
		widget = forms.TextInput(attrs={'size':'50'})
	)
	
	category = forms.CharField(
		required=True,
		label="Category",
		widget=forms.Select(choices=(
		    ('news', 'News'),
		    ('picture', 'Picture'),
		    ('story', 'Story'),
		))
	)
	
	class Meta:
		model = Link


class MainHandler(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
		
		query = Link.all(keys_only=True)
		
		if query.count() < 1:
			self.redirect('/no-links/')
		else:
			random_index = random.randint(0, query.count()-1 );
			
			link_key = query.fetch( 1, random_index )[0]
			link = Link.get(link_key)
			
			template_values = {
				'link': link,
			}
			self.response.out.write(template.render(path, template_values))


class CategoryHandler(webapp.RequestHandler):
	def get(self, category):
		
		query = Link.all(keys_only=True)
		query.filter("category =", category)
		
		if query.count() < 1:
			self.redirect('/no-links/')
		else:
			random_index = random.randint(0, query.count()-1 );
			
			link_key = query.fetch( 1, random_index )[0]
			link = Link.get(link_key)
			
			path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
			template_values = {
				'link': link,
			}
			self.response.out.write(template.render(path, template_values))


class AddLinkHandler(webapp.RequestHandler):
	
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/link_add.html')
		template_values = {
			'form': LinkForm(),
		}
		self.response.out.write(template.render(path, template_values))
	
	def post(self):
		
		form = LinkForm(data=self.request.POST)
		
		if form.is_valid():
			form.save()
			self.redirect('/links/')
		else:
			template_values = {
				'form': form,
			}
			path = os.path.join(os.path.dirname(__file__), 'templates/link_add.html')
			self.response.out.write(template.render(path, template_values))
		
		


class DeleteLinkHandler(webapp.RequestHandler):
	
	def get(self, link_key):
		path = os.path.join(os.path.dirname(__file__), 'templates/link_delete.html')
		
		link = Link.get(link_key)
		
		template_values = {
			'link': link,
		}
		self.response.out.write(template.render(path, template_values))

	def post(self, link_key):
		
		logging.info(self.request.get('submit'))
		
		if self.request.get('submit') == 'Delete':
			link_key = self.request.get('link_key')
			link = Link.get(link_key)
			link.delete()
			
		self.redirect('/links/')


class ListLinksHandler(webapp.RequestHandler):
	
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/link_list.html')
		
		links = Link.all()
		
		template_values = {
			'links': links,
		}
		self.response.out.write(template.render(path, template_values))


def main():
	application = webapp.WSGIApplication(
		[
			('/', MainHandler),
			('/links/add/', AddLinkHandler),
			('/link/add/', AddLinkHandler),
			('/links/', ListLinksHandler),
			('/links/([a-zA-Z0-9]*)/delete/', DeleteLinkHandler),
			('/category/([a-z]*)', CategoryHandler),
			('/category/([a-z]*)/', CategoryHandler),
		],
		debug=True
	)
	util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
