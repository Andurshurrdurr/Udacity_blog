from MainHandler import Handler

class logout(Handler): # Clears session cookies to log user out
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'username=;Path=/')
		self.response.headers.add_header('Set-Cookie', 'password=;Path=/')
		self.redirect('/login')
