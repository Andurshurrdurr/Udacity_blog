from MainHandler import Handler

class welcome(Handler): # Renders welcome page
	def get(self):
		user = self.request.cookies.get('username')
		self.render("welcome.html", user=user)
