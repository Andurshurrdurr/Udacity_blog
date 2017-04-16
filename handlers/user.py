from MainHandler import Handler

from context import Users

class user(Handler):  # Shows information about the specific user
	def get(self):
		uid = int(self.request.get('id'))
		user = Users.get_by_id(uid)
		self.render("user.html", user=user)
