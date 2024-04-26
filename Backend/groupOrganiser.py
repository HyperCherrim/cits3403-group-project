import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import Users, Groups, replyMessages

@app.shell_context_processor
def make_shell_context(): # Used for easier Flask *cookie monster noises* (Shell) sessions
    return{'alchemy':sa, 'orm':so, 'database':db, 'UserBase':Users, 'GroupBase':Groups, 'replies':replyMessages}