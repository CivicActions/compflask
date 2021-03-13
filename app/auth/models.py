from flask_login import UserMixin
from sqlalchemy.ext.declarative import DeclarativeMeta

from app import db

BaseModel: DeclarativeMeta = db.Model


# Define a base model for other database tables to inherit
class Base(BaseModel):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )


class User(UserMixin, Base):

    __tablename__ = "user"

    # User Name
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, name, email, password):

        self.name = name
        self.email = email
        self.password = password
        self.status = 1

    def __repr__(self):
        return "<User %r>" % (self.name)
