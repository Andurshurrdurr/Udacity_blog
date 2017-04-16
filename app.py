# Importing webapp package
import webapp2

# Importing handlers
from handlers.mainpage import mainpage
from handlers.login import login
from handlers.logout import logout
from handlers.signup import signup
from handlers.submit import submit
from handlers.welcome import welcome
from handlers.user import user
from handlers.post import post
from handlers.like import like
from handlers.comment import comment

# Routing to right handler
app = webapp2.WSGIApplication([	('/', mainpage),
								('/login', login),
								('/logout', logout),
								('/signup', signup),
								('/submit', submit),
								('/welcome', welcome),
								('/user', user),
								('/post', post),
								('/like', like),
								('/comment', comment)])
