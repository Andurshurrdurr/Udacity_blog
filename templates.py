import os

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'template_dir')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

# Requesthandlers

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Entry(db.Model):
	title = db.StringProperty(required=True)
	entry = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)

class MainPage(Handler):
	def renderself(self):
		entries = db.GqlQuery("SELECT * FROM Entry ORDER BY created DESC")
		self.render("front.html", entries=entries)

	def get(self):
		self.renderself()

	

class success(Handler):
	def get(self):
		id = int(self.request.get('id'))
		entry = Entry.get_by_id(id)
		self.render("success.html", entry=entry)

class submit(Handler):
	def get(self):
		self.render("submit.html")

	def post(self):
		title = self.request.get('title')
		entry = self.request.get('entry')
		if title and entry:
			e = Entry(title=title, entry=entry)
			e.put()
			self.redirect("success?id=%s" % e.key().id())
		else:
			self.render('submit.html', title=title, entry=entry, error="Supply valid input")


app = webapp2.WSGIApplication([('/', MainPage), ('/success', success), ('/submit', submit), ])

