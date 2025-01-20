from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128),nullable=False)
    email = db.Column(db.String(128),nullable=False)
    password = db.Column(db.String(128),nullable=False)
    collection = db.relationship("Collection", backref="user", lazy=True)

class Collection(db.Model):
    __tablename__="collection"
    id = db.Column(db.Integer, primary_key=True)
    name_of_item = db.Column(db.String(128),nullable=False)
    item_type = db.Column(db.String(128),nullable=False)
    item_price = db.Column(db.Float,nullable=False)
    item_description = db.Column(db.String(250),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)