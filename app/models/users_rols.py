from app import db
from flask import request
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models import user ,rol

class Users_rols(db.Model):
    ____tablename__ = 'users_rols'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rol_id = db.Column(db.Integer, db.ForeignKey('rols.id'))
    user = db.relationship('User', backref=db.backref("users_rols",cascade="all, delete-orphan"))
    rol = db.relationship('Rol', backref=db.backref("users_rols",cascade="all, delete-orphan"))

    def __init__(self, data):
        self.name = data['name']
        db.session.commit()
