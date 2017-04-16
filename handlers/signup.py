from MainHandler import Handler, hash_pass

from google.appengine.ext import db

from context import Users

import re


patterns = { # These are the RE for inputs
			'USER_RE': (r"^[a-zA-Z0-9_-]{3,20}$"),
			'PASS_RE': (r"^.{3,20}$"),
			'MAIL_RE': (r"^[\S]+@[\S]+.[\S]+$")
			}

def valid_field(field, value):  # Validates strings with RE
	return re.match(patterns[field], value)

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

		u = list(db.GqlQuery(
				"SELECT * FROM Users WHERE username = '%s'" % user_name))
		if len(u) != 0:  # Checks to see if username is taken
			invalid = True
			valid[0] = "Username already taken"
		else:
			pass

		if invalid == True: # Render invalid or redirect
			self.render("signup.html",
						error="Check your fields",
						usermsg=valid[0],
						passmsg=valid[1],
						verifymsg=valid[2],
						mailmsg=valid[3])
		else: # Hash password, new user in userdb and set cookie
			h = hash_pass(user_pass)
			u = Users(username=user_name, password=h)
			u.put()
			self.response.headers.add_header('Set-Cookie',
										'username=%(username)s;Path=/'
										% {'username':str(user_name)})
			self.response.headers.add_header('Set-Cookie',
										'password=%(password)s;Path=/'
										% {'password':str(h.split(',')[0])})
			self.redirect("/welcome")
