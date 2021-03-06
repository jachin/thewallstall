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

from controllers import mainh

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


class LoggedOutHandler(webapp.RequestHandler):

	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/loggedout.html')
		template_values = { }
		self.response.out.write(template.render(path, template_values))



def main():
	application = webapp.WSGIApplication(
		[
			('/', mainh.MainHandler),
			('/no-links/', mainh.NoLinksHandler),
			('/logout/', LoggedOutHandler),
			# ('/links/add/', AddLinkHandler),
			# ('/link/add/', AddLinkHandler),
			# ('/links/', ListLinksHandler),
			# 
			# ('/links/([a-zA-Z0-9]*)/delete/', DeleteLinkHandler),
			# ('/category/([a-z]*)', CategoryHandler),
			# ('/category/([a-z]*)/', CategoryHandler),
		],
		debug=True
	)
	util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
