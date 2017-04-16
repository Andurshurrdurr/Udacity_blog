from MainHandler import Handler
from google.appengine.ext import db

from context import Entries

class submit(Handler): # Submits a new blog entry
	def get(self): # Validates and renders submit form
		if self.validate_user_login():
			self.render("submit.html")
		else: # User not logged in -> Redirecting to login
			self.redirect("/login")

	def post(self): # Validates and posts a new entry
		if self.validate_user_login():
			title = self.request.get('title')
			entry = self.request.get('entry')
			if title and entry: # Submitted fields -> puts into db
				uid = cookie_user = self.request.cookies.get('username')
				u = list(db.GqlQuery(
						 "SELECT * FROM Users WHERE username = '%s'" % uid))
				u = u[0]
				e = Entries(user=u, title=title, entry=entry)
				e.put()
				print "Entry put in database. Redirecting ..."
				self.redirect("post?id=%s" % e.key().id()) # Redirects to post
			else:
				self.render('submit.html',
							title=title,
							entry=entry,
							error="Supply valid input")
