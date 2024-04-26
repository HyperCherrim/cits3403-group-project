import sqlalchemy as sa
import sqlalchemy.orm as so
#from flask_login import UserMixin # Will be used for verifying users
from typing import Optional
from datetime import datetime, timezone # Changing the date and time fields to instead be dateTime type
from app import db

class Users(db.Model):
    userID: so.Mapped[int] = so.mapped_column(primary_key=True)
    userEmail: so.Mapped[str] = so.mapped_column(sa.String(160), unique=True)
    hashedPassword: so.Mapped[str] = so.mapped_column(sa.String(255))
    creationDate: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))

class Groups(db.Model):
    groupID: so.Mapped[int] = so.mapped_column(primary_key=True)
    # fill in the userID later
    postCreationDate: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now()) # Just dealing with this temporarily
    tagOne: so.Mapped[str] = so.mapped_column(sa.String(8))
    tagTwo: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8)) # Some groups may only require one tag
    tagThree: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8)) 
    studentAvailability: so.Mapped[str] = so.mapped_column(sa.String(255))
    requiredStudents: so.Mapped[int] = so.mapped_column(sa.Integer())

class replyMessages(db.Model):
    messageID: so.Mapped[int] = so.mapped_column(primary_key=True)
    # Link to user (Users table referencing userID) - one user can have many messages, but one message belongs to one user
    # Also link to GroupReply - one user can reply to many groups, but one reply belongs to one user?
    message: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    messageCreationDate: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now()) # Type of the dateTime will depend on how it is being submitted
    availability: so.Mapped[str] = so.mapped_column(sa.String(128)) # Same here