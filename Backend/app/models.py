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
    groupMembership: so.Mapped[Optional[str]] = so.mapped_column(sa.String())
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
    requiredStudents: so.Mapped[int] = so.mapped_column(sa.Integer(), nullable=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255))
    timeslots = so.relationship('TimeSlot', backref='group', lazy=True)
    members: so.Mapped[str] = so.mapped_column(sa.String())

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class TimeSlot(db.Model):
    ID: so.Mapped[int] = so.mapped_column(primary_key=True)
    groupID: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Groups.groupID), index=True)
    userID: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Users.userID), index=True)
    day: so.Mapped[str] = so.mapped_column(sa.String(10))
    start_time = sa.Column(sa.Time, nullable=False)
    end_time = sa.Column(sa.Time, nullable=False)

    def __repr__(self):
        return f"<TimeSlot(day={self.day}, start_time={self.start_time}, end_time={self.end_time})>"
      
@login.user_loader
def load_user(userID):
    return db.session.get(Users, int(userID))
