import os

import re
import hashlib
import string
import random

import webapp2
import jinja2

from google.appengine.ext import db 

template_dir = os.path.join(os.path.dirname(__file__), 'template_dir') # Gets the template directory for jinja
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True) # Gets jinja dir

patterns = { # These are the RE for inputs
'USER_RE': (r"^[a-zA-Z0-9_-]{3,20}$"),
'PASS_RE': (r"^.{3,20}$"),
'MAIL_RE': (r"^[\S]+@[\S]+.[\S]+$")
}

# Databases

class Users(db.Model): # Users DB class
	username = db.StringProperty(required=True)
	password = db.StringProperty(required=True)
	joined = db.DateTimeProperty(auto_now_add=True)

class Entries(db.Model): # Blog entry DB class
	user = db.ReferenceProperty(Users, 
								collection_name='entries', required=True)
	title = db.StringProperty(required=True)
	entry = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	likes = db.IntegerProperty(default=0)

class Comments(db.Model): # Comments DB class
	entry = db.ReferenceProperty(Entries,
								collection_name='comments', required=True)
	user = db.ReferenceProperty(Users, 
								collection_name='comments', required=True)
	comment = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add=True)

class Likers(db.Model): # Likers DB class: ties users who likes with entries they like
	entry = db.IntegerProperty(required=True)
	user = db.StringProperty(required=True)

# --------------------------------------------- Helperfunctions ----------------------------------------------------------

def valid_field(field, value): # Checks to see if a string is valid based on RE
	return re.match(patterns[field], value)

def make_new_salt(): # Function that returns a new salt
	alphabet = string.letters
	s = ""
	for i in range(0, 5):
		s += random.choice(alphabet)
	return s 

def hash_pass(user_pass, s=""): # Function that hashes passwords 
	if s =="":
		s = make_new_salt()
	else:
		pass
	h = hashlib.sha256(user_pass + 'SECRET' + s).hexdigest() + ',' + s
	return h

def validate_pass(passwrd, h): # Get plain password and hash+salt, returns true with valid match
	if hash_pass(passwrd, h.split(',')[1]).split(',')[0] == h.split(',')[0]:
		return True
	else:
		return False

def validate_user(username, **kw): # Get cookie username and hash/passwrd, validates with user db, returns False if invalid
	u = list(db.GqlQuery("SELECT * FROM Users WHERE username = '%s'" % username)) # User instance getter
	if len(u) != 0: # User in DB?
		if kw['h'] and u[0].password.split(',')[0] == kw['h']: # If supplied a hash
			return True # Returns true if hash is correct
		elif validate_pass(kw['passwrd'], u[0].password): # If supplied a password
			return str(u[0].password.split(',')[0]) # Returns hash (not salt) for password
		else:
			return False
	else:
		False

# --------------------------------------------- Main handler -------------------------------------------------------------

class Handler(webapp2.RequestHandler): # Main handler
	def validate(self): # Validates user based on cookies, returns username if true, redirects to login if false
		cookie_user = self.request.cookies.get('username')
		cookie_h = self.request.cookies.get('password')
		if validate_user(cookie_user, h=cookie_h, passwrd=""):
			return cookie_user
		else:
			self.redirect('/login')

	def write(self, *a, **kw): # Output to user
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params): # Renders template with params
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw): # Renders template with arguments, checks for user login and renders appropriately
		usertop = self.request.cookies.get('username')
		kw['usertop'] = usertop
		self.write(self.render_str(template, **kw))

# --------------------------------------------- Handlers for each page after this comment --------------------------------

class MainPage(Handler): # Handler for / - Renders all entries
	def get(self):
		entries = db.GqlQuery("SELECT * FROM Entries ORDER BY created DESC")
		self.render("front.html", entries=entries)

class user(Handler): # Shows information about the specific user
	def get(self):
		uid = int(self.request.get('id'))
		user = Users.get_by_id(uid)
		self.render("user.html", user=user)

class post(Handler): # Shows info and options for specific blogpost
	def get(self):
		post_id = int(self.request.get('id'))
		entry = Entries.get_by_id(post_id)
		comment = self.request.get('comment')
		user = self.validate()
		error = ""

		if comment: # Got comment
			if user == entry.user.username: # User who likes is the same who posted the post
				error = "Cannot comment your own post"
			elif user: # Other user
				Comments(entry=entry, user=list(db.GqlQuery("SELECT * FROM Users WHERE username = '%s'" % user))[0], 
						comment=comment).put()
				print "added comment " + comment
			else: # User not logged in -> Redirecting to login
				self.redirect("/login")
		elif self.request.get('like'): # Got like
			if user == entry.user.username: # User who likes is the same who posted the post
				error = "Cannot like your own post"

			elif user: # Not original poster
				llist = list(db.GqlQuery("SELECT * FROM Likers WHERE entry = %i" % post_id)) # Getting all users who liked post
				liked = False
				for l in llist: # Checking if current user is among likers
					if user == l.user:
						liked = True
				if liked == False: # If user hasnt already liked it, then post gets a new like
					l = Likers(entry=post_id, user=user).put()
					entry.likes += 1
					entry.put()
				else: 
					error = "You already liked this post"
			else: # User not logged in -> Redirecting to login
				self.redirect("/login")

		op = False
		if entry.user.username == user: # Check to see if user is original poster (op)
			op = True
			print "User is OP"
		print entry.user.key().id()

		comments = list(db.GqlQuery("SELECT * FROM Comments ORDER BY created DESC")) # Get comments
		clist = []
		for c in comments: # Filter out only comments belonging to this post
			if c.entry.key().id() == post_id:
				clist.append(c)

		likes = str(entry.likes) # Get likes
		self.render("post.html", op=op, entry=entry, likes=likes, comments=clist, error=error)
	
	def post(self): # Post handles updates to the blog entry
		user = self.validate()
		if user:
			entry = Entries.get_by_id(int(self.request.get('id')))
			print "entry ok"
			if entry.user.username == user: # Validation up till here
				if self.request.get("delete") == "Delete":
					entry.delete()
					self.redirect('/')
				else:
					entry.title = self.request.get("title")
					entry.entry = self.request.get("entry")
					entry.put()
		else: # User not logged in -> Redirecting to login
			self.redirect("/login")

class submit(Handler): # Submits a new blog entry
	def get(self): # Validates and renders submit form
		if self.validate():
			self.render("submit.html")
		else: # User not logged in -> Redirecting to login
			self.redirect("/login")

	def post(self): # Validates and posts a new entry
		if self.validate(): 
			title = self.request.get('title')
			entry = self.request.get('entry')
			if title and entry: # Submitted fields -> puts into db
				uid = cookie_user = self.request.cookies.get('username') 
				u = list(db.GqlQuery("SELECT * FROM Users WHERE username = '%s'" % uid))
				u = u[0]
				e = Entries(user=u, title=title, entry=entry)
				e.put()
				print "Entry put in database. Redirecting ..."
				self.redirect("post?id=%s" % e.key().id()) # Redirects to new post
			else:
				self.render('submit.html', title=title, entry=entry, error="Supply valid input") 

class signup(Handler): # Lets new users sign up
	def get(self): # Renders form
		self.render("signup.html")

	def post(self): # Gets new user
		user_name = self.request.get('username')
		user_pass = self.request.get('password')
		user_verify = self.request.get('verify')
		user_mail = self.request.get('email')

		valid = ['na1', 'na2', 'na3', 'na4'] # Validations list
		valid[0] = valid_field('USER_RE', user_name)
		valid[1] = valid_field('PASS_RE', user_pass)
		valid[3] = valid_field('MAIL_RE', user_mail)
		
		invalid = False
		incr = 0

		for na in valid: # Checks validations
			if na == None:
				na = "Invalid input"
				invalid = True
			else:
				na = ""
			valid[incr] = na
			incr += 1

		if user_pass != user_verify: # Check password match
			valid[2] = "Passwords must match"
			invalid = True

		u = list(db.GqlQuery("SELECT * FROM Users WHERE username = '%s'" % user_name)) # Checks if username is taken
		if len(u) != 0:
			invalid = True
			valid[0] = "Username already taken"
		else: 
			pass

		if invalid == True: # Render invalid or redirect
			self.render("signup.html", error="Check your fields", usermsg=valid[0], passmsg=valid[1], verifymsg=valid[2], mailmsg=valid[3])
		else: # Hash password, make new user database entry and set session cookie
			h = hash_pass(user_pass)
			u = Users(username=user_name, password=h)
			u.put()
			self.response.headers.add_header('Set-Cookie', 'username=%(username)s;Path=/' 
												% {'username':str(user_name)})
			self.response.headers.add_header('Set-Cookie', 'password=%(password)s;Path=/' 
												% {'password':str(h.split(',')[0])})
			self.redirect("/welcome")

class login(Handler): # Lets existing users login
	def get(self): # Render login form
		self.render('login.html')

	def post(self): # Gets login cridentials and validates 
		user_name = self.request.get('username')
		user_pass = self.request.get('password')
		valid = validate_user(user_name, passwrd=user_pass, h="") # Validate user against db
		if valid: # Sets cookies and redirects to welcome page
			self.response.headers.add_header('Set-Cookie', 'username=%(username)s;Path=/' 
											% {'username':str(user_name)})
			self.response.headers.add_header('Set-Cookie', 'password=%(password)s;Path=/' 
											% {'password':valid})
			self.redirect('/welcome')
		else: 
			self.render('login.html', error="Invalid login")

class logout(Handler): # Logs the user out by clearing cookies and redirects to login
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'username=;Path=/')
		self.response.headers.add_header('Set-Cookie', 'password=;Path=/')
		self.redirect('/login')
		
class welcome(Handler): # Renders welcome page
	def get(self):
		user = self.request.cookies.get('username')
		self.render("welcome.html", user=user)

app = webapp2.WSGIApplication([	('/', MainPage), # For routing URL to right handler
								('/login', login),
								('/logout', logout), 
								('/signup', signup), 
								('/submit', submit), 
								('/welcome', welcome), 
								('/user', user),
								('/post', post)])

