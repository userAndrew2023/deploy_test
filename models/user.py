from datetime import datetime

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String(100))
    name = sqlalchemy.Column(sqlalchemy.String(100))
    age = sqlalchemy.Column(sqlalchemy.Integer)
    position = sqlalchemy.Column(sqlalchemy.String(100))
    speciality = sqlalchemy.Column(sqlalchemy.String(100))
    address = sqlalchemy.Column(sqlalchemy.String(200))
    email = sqlalchemy.Column(sqlalchemy.String(120), unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String(200))
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow, nullable=True)

    def __repr__(self):
        return f"<User {self.surname} {self.name}>"

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
