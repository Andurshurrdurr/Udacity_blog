import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(
                        os.path.dirname(__file__), '..')))

from models.entry import Entries
from models.comment import Comments
from models.liker import Likers
from models.user import Users
