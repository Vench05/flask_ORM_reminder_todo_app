import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin
from sqlalchemy.orm import backref

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(50), nullable = False)
    lname = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(250), unique = True, nullable = False)
    gender = db.Column(db.String(10), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    title = db.relationship('Title', backref="user", lazy=True)

    def add_title(self, title):
        title = Title(title = title, user_id = self.id)
        db.session.add(title)
        db.session.commit()

class Title(UserMixin, db.Model):
    __tablename__ = "titles"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    date = db.Column(db.DateTime, default = datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable = False)
    task = db.relationship('Task', backref=backref("Task.id", uselist=False))

    def add_task(self, task_add):
        task_add = Task(task = task_add, title_id = self.id)
        db.session.add(task_add)
        db.session.commit()

class Task(UserMixin, db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key = True)
    done = db.Column(db.Integer, default = 0)
    task = db.Column(db.String(250), nullable = False)
    title_id = db.Column(db.Integer, db.ForeignKey(Title.id), nullable = False)
