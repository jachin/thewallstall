from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class AdminHandler(webapp.RequestHandler):
	def get( self ):
		self.redirect('/admin/')

application = webapp.WSGIApplication(
	[
		('/admin', AdminHandler),
	]
)

def main():
   run_wsgi_app(application)

if __name__ == "__main__":
    main()