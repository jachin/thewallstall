#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import cgi
import os
import string
import logging
import random


class Link(db.Model):
	url = db.LinkProperty()
	category = db.CategoryProperty()


class MainHandler(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
		
		query = Link.all(keys_only=False)
		
		if query.count() < 1:
			self.redirect('/no-links/')
		
		random_index = random.randint(0, query.count()-1 );
		
		link = query.fetch( 1, random_index )[0]
		
		template_values = {
			'link': link,
		}
		self.response.out.write(template.render(path, template_values))

class LinkHandler(webapp.RequestHandler):
	def get(self, category):
		
		logging.info(category)
		
		path = os.path.join(os.path.dirname(__file__), 'templates/link.html')
		template_values = {
			'url': 'http://clockwork.net',
		}
		self.response.out.write(template.render(path, template_values))


class AddLinkHandler(webapp.RequestHandler):
	
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/add_link.html')
		template_values = {
			
		}
		self.response.out.write(template.render(path, template_values))
	
	def post(self):
		url = self.request.get('url')
		category = self.request.get('category')
		
		link = Link()
		link.url = db.Link(url)
		link.category = db.Category(category)
		link.put()
		
		self.redirect('/links/')


class DeleteLinkHandler(webapp.RequestHandler):

	def get(self, link_key):
		path = os.path.join(os.path.dirname(__file__), 'templates/delete_link.html')
		
		link = Link.get(link_key)
		
		template_values = {
			'link': link,
		}
		self.response.out.write(template.render(path, template_values))

	def post(self, link_key):
		
		logging.info(self.request.get('submit'))
		
		if self.request.get('submit') is not 'Delete':
			self.redirect('/links/')
		
		link_key = self.request.get('link_key')
		link = Link.get(link_key)
		link.delete()
		
		self.redirect('/links/')


class ListLinksHandler(webapp.RequestHandler):
	
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/list_links.html')
		
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
			('/category/([a-z]*)', LinkHandler),
			('/category/([a-z]*)/', LinkHandler),
		],
		debug=True
	)
	util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
