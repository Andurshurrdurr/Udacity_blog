from google.appengine.ext import db

class Users(db.Model):  # Users DB class
	username = db.StringProperty(required=True)
	password = db.StringProperty(required=True)
	joined = db.DateTimeProperty(auto_now_add=True)
