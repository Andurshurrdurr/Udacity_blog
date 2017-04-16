from google.appengine.ext import db
from user import Users
from entry import Entries

class Comments(db.Model):  # Comments DB class
	entry = db.ReferenceProperty(Entries,
								collection_name='comments', required=True)
	user = db.ReferenceProperty(Users,
								collection_name='comments', required=True)
	comment = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add=True)
