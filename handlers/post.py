from MainHandler import Handler, post_exists
from google.appengine.ext import db

from context import Entries
from context import Comments
from context import Likers

class post(Handler):
	"""Shows info and options for specific blogpost. 4 step process:
	1. Check if post exist
	2. Check if user is logged in
	3. Check if user == author of post
	4. Do something
	"""
	@post_exists
	def get(self, post_id):
		user = self.validate_user_login()
		entry = Entries.get_by_id(post_id)
		error = self.request.get('error')

		if entry.user.username == user:  # Check if user is author
			author = True
		else:
			author = False
		comments = list(db.GqlQuery(
						"SELECT * FROM Comments ORDER BY created DESC"))
		clist = []
		for c in comments: # Filter out only comments belonging to this post
			if c.entry.key().id() == post_id:
				clist.append(c)
			else:
				pass
		likes = str(entry.likes) # Get likes
		self.render("post.html",
					op=author,
					user=user,
					entry=entry,
					likes=likes,
					comments=clist,
					error=error)
	@post_exists
	def post(self, post_id): # Post handles updates to the blog entry
		user = self.validate_user_login()
		entry = Entries.get_by_id(int(self.request.get('id')))
		print "entry ok"
		if entry.user.username == user: # user == author
			if self.request.get("delete") == "Delete": # User want to delete
				entry.delete()
			else: # User wants to update post
				entry.title = self.request.get("title")
				entry.entry = self.request.get("entry")
				entry.put()
			self.render("updated.html") # Success!
		else:
			self.redirect("/") # User != author
