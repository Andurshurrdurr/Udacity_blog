from MainHandler import Handler
from google.appengine.ext import db

class mainpage(Handler):  # Handler for / - Renders all entries
	def get(self):
		entries = db.GqlQuery("SELECT * FROM Entries ORDER BY created DESC")
		self.render("front.html", entries=entries)
