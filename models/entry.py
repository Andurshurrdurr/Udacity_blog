from google.appengine.ext import db
from user import Users

class Entries(db.Model):  # Blog entry DB class
	user = db.ReferenceProperty(Users,
								collection_name='Entries', required=True)
	title = db.StringProperty(required=True)
	entry = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	@property
	def likes(self):
		"""return the number of likes for this post"""
		llist = list(db.GqlQuery(  # Getting all users who liked post
			"SELECT * FROM Likers WHERE entry = %i" % self.key().id()))
		return len(llist)
