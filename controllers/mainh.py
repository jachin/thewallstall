#!/usr/bin/env python

import os
import random

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms

from django import forms

from models.models import Link

class MainHandler(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), '../templates/main.html')
		
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
		
	


class NoLinksHandler(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), '../templates/no_links.html')
		template_values = { }
		self.response.out.write(template.render(path, template_values))
	

