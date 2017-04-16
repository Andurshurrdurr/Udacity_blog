import MainHandler

class login(MainHandler.Handler): # Lets existing users login
	def get(self): # Render login form
		self.render('login.html')

	def post(self): # Gets login cridentials and validates
		user_name = self.request.get('username')
		user_pass = self.request.get('password')
		valid = MainHandler.validate_user(user_name, passwrd=user_pass, h="")
		if valid: # Sets cookies and redirects to welcome page
			self.response.headers.add_header('Set-Cookie',
										'username=%(username)s;Path=/'
										% {'username':str(user_name)})
			self.response.headers.add_header('Set-Cookie',
										'password=%(password)s;Path=/'
										% {'password':valid})
			self.redirect('/welcome')
		else:
			self.render('login.html', error="Invalid login")
