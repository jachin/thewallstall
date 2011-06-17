#!/usr/bin/env python

from google.appengine.ext import db

class Link(db.Model):
	url = db.LinkProperty(required=True)
	category = db.CategoryProperty(required=True)