from google.appengine.ext import db

class Likers(db.Model):  # Likers DB class: ties likers with entries
	entry = db.IntegerProperty(required=True)
	user = db.StringProperty(required=True)
