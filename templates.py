import os

import re
import hashlib
import string
import random

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'template_dir')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

patterns = {
'USER_RE': (r"^[a-zA-Z0-9_-]{3,20}$"),
'PASS_RE': (r"^.{3,20}$"),
'MAIL_RE': (r"^[\S]+@[\S]+.[\S]+$")
}

# Databases

class Users(db.Model): # DB class, takes username and password hash
	username = db.StringProperty(required=True)
	password = db.StringProperty(required=True)
	joined = db.DateTimeProperty(auto_now_add=True)

class Entries(db.Model):
	title = db.StringProperty(required=True)
	entry = db.TextProperty(required=True)
	#submitterid = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)

# Helperfunctions

def valid_field(field, value):
	return re.match(patterns[field], value)

def make_new_salt():
	alphabet = string.letters
	s = ""
	for i in range(0, 5):
		s += random.choice(alphabet)
	return s

def hash_pass(user_pass, s=""):
	if s =="":
		s = make_new_salt()
	else:
		pass
	h = hashlib.sha256(user_pass + 'SECRET' + s).hexdigest() + ',' + s
	return h

def validate_pass(passwrd, h): # Get plain password and hash
	if hash_pass(passwrd, h.split(',')[1]).split(',')[0] == h.split(',')[0]:
		return True
	else:
		return False

def validate_user(username, **kw): # Get cookie username and hash, check in db
	u = list(db.GqlQuery("SELECT * FROM Users WHERE username = '%s'" % username))
	if len(u) != 0: # User in DB?
		print "User in db, checking validation for passhash: "
		print u[0].password
		# Cookie hash:
		print "password is: "+kw['passwrd']
		print "hash is: "+kw['h']
		if kw['h'] and u[0].password.split(',')[0] == kw['h']: 
			return True
		elif validate_pass(kw['passwrd'], u[0].password):
			return str(u[0].password.split(',')[0])
		else:
			return False
	else:
		False



# Requesthandler

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

# Pages

class MainPage(Handler):
	def renderself(self):
		entries = db.GqlQuery("SELECT * FROM Entries ORDER BY created DESC")
		self.render("front.html", entries=entries)

	def get(self):
		self.renderself() # Add a way to like / comment / access posts

class user(Handler): 
	def get(self):
		id = int(self.request.get('id'))
		user = Users.get_by_id(id)
		self.render("user.html", user=user)

class post(Handler): # Pretty much the same as the user handler
	def get(self):
		id = int(self.request.get('id'))
		entry = Entries.get_by_id(id)
		self.render("post.html", entry=entry)

class submit(Handler):
	def validate(self):
		cookie_user = self.request.cookies.get('username')
		cookie_h = self.request.cookies.get('password')
		if validate_user(cookie_user, h=cookie_h, passwrd=""):
			return True
		else:
			self.redirect('/login')

	def get(self):
		if self.validate():
			self.render("submit.html")

	def post(self):
		# validate -> if not auth => redirect to login/signup
		if self.validate():
			print "posting entry"
			title = self.request.get('title')
			entry = self.request.get('entry')
			print "Got entry input: " + title + entry
			if title and entry:
				print "Putting into database ... "
				e = Entries(title=title, entry=entry)
				e.put()
				print "Entry put in database. Redirecting ..."
				self.redirect("post?id=%s" % e.key().id())
			else:
				self.render('submit.html', title=title, entry=entry, error="Supply valid input") # TODO -> SUBMITTER ID

class signup(Handler): # TODO: Limit usernames
	def get(self):
		self.render("signup.html")

	def post(self):
		user_name = self.request.get('username')
		user_pass = self.request.get('password')
		user_verify = self.request.get('verify')
		user_mail = self.request.get('email')

		valid = ['na1', 'na2', 'na3', 'na4']
		valid[0] = valid_field('USER_RE', user_name)
		valid[1]= valid_field('PASS_RE', user_pass)
		valid[3] = valid_field('MAIL_RE', user_mail)
		
		invalid = False
		incr = 0
		for na in valid:
			if na == None:
				na = "Invalid input"
				invalid = True
			else:
				na = "All good here"
			valid[incr] = na
			incr += 1


		# Check password match
		if user_pass != user_verify:
			valid[2] = "Passwords must match"
			invalid = True

		# Render invalid or redirect
		if invalid == True:
			self.render("signup.html", error="Check your fields", usermsg=valid[0], passmsg=valid[1], verifymsg=valid[2], mailmsg=valid[3])
		else: 
			# Hash password, make user database entry and set cookie
			h = hash_pass(user_pass)
			u = Users(username=user_name, password=h)
			u.put()
			self.response.headers.add_header('Set-Cookie', 'username=%(username)s;Path=/' 
												% {'username':str(user_name)})
			self.response.headers.add_header('Set-Cookie', 'password=%(password)s;Path=/' 
												% {'password':str(h.split(',')[0])})
			self.redirect("/welcome")

class login(Handler): #OK
	def get(self):
		self.render('login.html')

	def post(self):
		user_name = self.request.get('username')
		user_pass = self.request.get('password')
		valid = validate_user(user_name, passwrd=user_pass, h="")
		if valid:
			self.response.headers.add_header('Set-Cookie', 'username=%(username)s;Path=/' 
											% {'username':str(user_name)})
			self.response.headers.add_header('Set-Cookie', 'password=%(password)s;Path=/' 
											% {'password':valid})
			self.redirect('/welcome')
		else:
			self.render('login.html', error="Invalid login")

class logout(Handler): #OK
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'username=;Path=/')
		self.response.headers.add_header('Set-Cookie', 'password=;Path=/')
		self.redirect('/signup')
		
class welcome(Handler): #OK
	def get(self):
		#get cookie
		user = self.request.cookies.get('username')
		#render site
		self.render("welcome.html", user=user)

app = webapp2.WSGIApplication([	('/', MainPage), 
								('/login', login),
								('/logout', logout), 
								('/signup', signup), 
								('/submit', submit), 
								('/welcome', welcome), 
								('/user', user),
								('/post', post)])

