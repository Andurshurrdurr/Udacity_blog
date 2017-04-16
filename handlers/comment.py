from MainHandler import Handler, post_exists, comment_exists
from google.appengine.ext import db

from context import Entries
from context import Comments

class comment(Handler):
    """Handler for commenting on posts"""
    @comment_exists
    def post(self, post_id, com):
        """Gets the post_id and user, checks with db"""
        user = self.validate_user_login()
        entry = Entries.get_by_id(post_id)
        comment = self.request.get('comment')
        error = ""
        updated = False
        if user == entry.user.username:  # Check to see commenter = post_author
            error="Cannot comment your own post"
        elif comment == "":
            error = "Invalid comment"
        else:  # Other user
            if com: # Editing commend, update in db
                if com.user.username == user: # User == comment author
                    if self.request.get("delete"): # Delete comment
                        com.delete()
                    else: # Edit comment
                        com.comment = comment
                        com.put()
                    updated = True
                else: # Not valid
                    error="Youre not the author of the comment"
            else: # New comment
                Comments(entry=entry, user=list(db.GqlQuery(
                        "SELECT * FROM Users WHERE username = '%s'"
                        % user))[0],comment=comment).put()
                updated = True

        if updated == True:
			self.render("updated.html")
        else:
            self.redirect("/post?id=%s&error=%s" % (post_id, error))
