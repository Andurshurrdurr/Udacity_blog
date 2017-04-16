from MainHandler import Handler, post_exists
from google.appengine.ext import db

from context import Entries
from context import Likers

class like(Handler):
    """Handler for liking posts"""
    @post_exists
    def get(self, post_id):
        user = self.validate_user_login()
        entry = Entries.get_by_id(post_id)
        error = ""
        if user == entry.user.username:  # Check to see liker = author
            error = "Cannot like your own post"
        else:  # Not original poster
            llist = list(db.GqlQuery(  # Getting all users who liked post
                "SELECT * FROM Likers WHERE entry = %i" % post_id))
            liked = False
            for l in llist: # Checking if current user is among likers
                if user == l.user:
                    liked = True
            if liked == False: # Check if post already liked by user
                l = Likers(entry=post_id, user=user).put()
                entry.put()
                self.render("updated.html")
            else:
                error = "You already liked this post"
        self.redirect("/post?id=%s&error=%s" % (post_id, error))
