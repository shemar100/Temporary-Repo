import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date


database_path = 'postgresql://postgres:root@localhost/test'

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:root@localhost/test'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_createdrop_all():
    db.drop_all()
    db.create_all()


def db_init_records():
    new_actor = Actor(
        name = 'Matthew',
        gender = 'Male',
        age = 25
    )

    new_movie = (Movie(
        title = 'movie',
        release_date = date.today()
    ))


    table = Table.insert().values(
        Movie_id = new_movie.id,
        Actor_id = new_actor.id,
        actor_fee = 500.00
    )

    new_actor.create()
    new_movie.create()
    db.session.execute(table)
    db.session.commit()

Table = db.Table('Table', db.Model.metadata,
    db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('Actor_id', db.Integer, db.ForeignKey('actors.id')),
    db.Column('actor_fee', db.Float)
)


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True)
    gender = Column(String(200))
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    release_date = Column(Date)
    actors = db.relationship('Actor', secondary=Table, backref=db.backref(
        'tables', lazy='joined'))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
