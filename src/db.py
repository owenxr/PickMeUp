from flask_sqlalchemy import SQLAlchemy
import datetime
import hashlib
import os
import bcrypt

db = SQLAlchemy()

# Link Categories to Users, Many to Many

association_table = db.Table("association", db.Model.metadata,
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

###
###     TABLES
###

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    users = db.relationship("User", secondary=association_table, back_populates="categories")
    data = db.relationship("Data", cascade="delete")

    def __init__(self,**kwargs):
        self.name = kwargs.get("category")

    def serialize(self):
        return {
            "id": self.id,
            "category": self.name
        }


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key =True)
    category = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    photo = db.Column(db.String(length=10000), nullable=False)
    photographer = db.Column(db.String(length=500), nullable=False)
    
    def __init__(self, **kwargs):
        self.photo = kwargs.get("photo")
        self.photographer = kwargs.get("photographer")
        self.category = kwargs.get("category")

    def serialize(self):
        return {
            "id": self.id,
            "category": Category.query.filter_by(id=self.category).first().name,
            "photo": self.photo,
            "photographer": self.photographer + " - Uploaded to Pexel Photos"
        }

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(length=50), nullable=False)
    password_digest = db.Column(db.String(length=500), nullable=False)
    email = db.Column(db.String(length=70), nullable=False)
    categories = db.relationship("Category", secondary=association_table, back_populates='users')

    session_token = db.Column(db.String(length=500), nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String(length=500), nullable=False, unique=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.password_digest = bcrypt.hashpw(kwargs.get("password").encode("utf8"), bcrypt.gensalt(rounds=13))
        self.renew_session()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "categories": [c.serialize() for c in self.categories]
        }

    def session(self):
        return {
            "id": self.id,
            "session_token": self.session_token,
            "session_expiration": str(self.session_expiration),
            "update_token": self.update_token
        }


###
###     Variables for Session Authentication
###

    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest.encode("utf8"))

    def verify_session_token(self, session_token):
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        return update_token == self.update_token

        
