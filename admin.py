#!/usr/bin/env python

from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from google.appengine.api.users import create_logout_url

from django import forms

import cgi
import os
import string
import logging
import random

from models.models import Link

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



class ListLinksHandler(webapp.RequestHandler):
	
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/link_list.html')
		
		links = Link.all()
		
		template_values = {
			'logout_url': create_logout_url('/admin/logout/'),
			'links': links,
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
			self.redirect('/admin/links/')
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
		
		if self.request.get('submit') == 'Delete':
			link_key = self.request.get('link_key')
			link = Link.get(link_key)
			link.delete()
		
		self.redirect('/admin/links/')


def main():
	application = webapp.WSGIApplication(
		[
			('/admin/', ListLinksHandler),
			('/admin/links/add/', AddLinkHandler),
			('/admin/link/add/', AddLinkHandler),
			('/admin/links/', ListLinksHandler),
			('/admin/links/([a-zA-Z0-9]*)/delete/', DeleteLinkHandler),
		],
		debug=True
	)
	util.run_wsgi_app(application)


if __name__ == '__main__':
    main()