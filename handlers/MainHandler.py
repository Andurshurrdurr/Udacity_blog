import os

import hashlib
import string
import random

import webapp2
import jinja2

from google.appengine.ext import db

# ----- Declaring the jinja environment --------

template_dir = os.path.join(os.path.dirname(__file__), '../template_dir')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                                template_dir), autoescape=True)

# ------ Helper functions for validation -------

def make_new_salt():  # Function that returns a new salt
	alphabet = string.letters
	s = ""
	for i in range(0, 5):
		s += random.choice(alphabet)
	return s

def hash_pass(user_pass, s=""):  # Function that hashes passwords
	if s =="":
		s = make_new_salt()
	else:
		pass
	h = hashlib.sha256(user_pass + 'SECRET' + s).hexdigest() + ',' + s
	return h

def validate_pass(passwrd, h):  # Get plain password and hash+salt
	if hash_pass(passwrd, h.split(',')[1]).split(',')[0] == h.split(',')[0]:
		return True
	else:
		return False

def validate_user(username, **kw):  # Get cookie, validate with db
	u = list(db.GqlQuery(
				"SELECT * FROM Users WHERE username = '%s'" % username))
	if len(u) != 0:  # User in DB?
		if kw['h'] and u[0].password.split(',')[0] == kw['h']:  # If hash
			return True  # Returns true if hash is correct
		elif validate_pass(kw['passwrd'], u[0].password):  # If password
			return str(u[0].password.split(',')[0])  # Returns hash
		else:
			return False
	else:
		return False

# ------ Handler for all handlers ------

class Handler(webapp2.RequestHandler):
	"""This is the main handler parent with functions for all handlers."""
	def validate_user_login(self):
		"""Validates user login based on cookies.
		Returns username (from cookie) if true, redirects to login if false.
		"""
		cookie_user = self.request.cookies.get('username')
		cookie_h = self.request.cookies.get('password')
		if validate_user(cookie_user, h=cookie_h, passwrd=""):
			return cookie_user
		else:
			self.redirect('/login')

	def write(self, *a, **kw):
		"""Simple output to user"""
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		"""Renders template with params."""
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		"""Renders template with arguments"""
		usertop = self.request.cookies.get('username')
		kw['usertop'] = usertop
		self.write(self.render_str(template, **kw))

# ----- Decorators -------

def post_exists(f): # Decorator to check if post exist
    def wrapped(self):
        print "Checking to see if post exists..."
        post_id = int(self.request.get('id'))
        key = db.Key.from_path('Entries', post_id)
        post = db.get(key)
        if post:
            return f(self, post_id)
        else:
            self.error(404)
            return self.redirect("/")
    return wrapped

def comment_exists(f): # Decorator to check if post exist
    @post_exists
    def wrapped_post(self, post_id):
        try:
            cid = self.request.get('cid')
            cid = int(cid)
            key = db.Key.from_path('Comments', int(cid))
            com = db.get(key)
        except:
            com = False
        finally:
            return f(self, post_id, com)
    return wrapped_post
