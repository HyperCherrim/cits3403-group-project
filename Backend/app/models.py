import sqlalchemy as sa # SQL Operations
import sqlalchemy.orm as so

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


from werkzeug.security import generate_password_hash, check_password_hash # Password security checking - may not be needed yet
from flask_login import UserMixin # Will be used for verifying users
from typing import Optional
from datetime import datetime, timezone # Changing the date and time fields to instead be dateTime type
from app import db, login # Load the database and forms


engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

class Users(UserMixin, db.Model):
    userID: so.Mapped[int] = so.mapped_column(primary_key=True)
    fullName: so.Mapped[str] = so.mapped_column(sa.String(150))
    userName: so.Mapped[int] = so.mapped_column(sa.Integer(), unique=True)
    userEmail: so.Mapped[str] = so.mapped_column(sa.String(160), unique=True)
    userPasswords: so.Mapped[Optional[str]] = so.mapped_column(sa.String(254))
    creationDate: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    def __repr__(self):
        return '<User {}>'.format(self.userName)
    def setPassword(self, studentPW):
        self.userPasswords = generate_password_hash(studentPW)
    def getPassword(self, studentPW):
        return check_password_hash(self.userPasswords, studentPW)
    def get_id(self):
        return(self.userID)

class Groups(db.Model):
    groupID: so.Mapped[int] = so.mapped_column(primary_key=True)
    userID: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Users.userID), index=True)
    postCreationDate: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now()) # Just dealing with this temporarily
    groupTitle: so.Mapped[str] = so.mapped_column(sa.String(255))
    tagOne: so.Mapped[str] = so.mapped_column(sa.String(8))
    tagTwo: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8)) # Some groups may only require one tag
    tagThree: so.Mapped[Optional[str]] = so.mapped_column(sa.String(8)) 
    studentAvailability: so.Mapped[str] = so.mapped_column(sa.String(255))
    requiredStudents: so.Mapped[int] = so.mapped_column(sa.Integer())
    mondayStartTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    mondayEndTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    tuesdayStartTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    tuesdayEndTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    webnesdayStartTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    webnesdayEndTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    thursdayStartTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    thursdayEndTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    fridayStartTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    fridayEndTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    saterdayStartTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    saterdayEndTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    sundayStartTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    sundayEndTime: so.Mapped[str] = so.mapped_column(sa.String(16))
    def __repr__(self):
        return '<Post {}>'.format(self.body)

class ReplyMessages(db.Model):
    messageID: so.Mapped[int] = so.mapped_column(primary_key=True)
    userID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Users.userID))
    # Also link to GroupReply - one user can reply to many groups, but one reply belongs to one user?
    requestID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Groups.groupID))
    message: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    messageCreationDate: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now()) # Type of the dateTime will depend on how it is being submitted
    availability: so.Mapped[str] = so.mapped_column(sa.String(128)) # Same here

@login.user_loader
def load_user(userID):
    return db.session.get(Users, int(userID))
