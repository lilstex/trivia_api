import os
from sqlalchemy import Column, ForeignKey, String, Integer, create_engine
from sqlalchemy.orm import declarative_base, relationship
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()

database_path = os.environ.get('DATABASE_URI')

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    
    migrate = Migrate(app, db)

"""
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    questions = relationship('Question', backref='category', lazy=True, cascade='all, delete-orphan')

    def __init__(self, type):
        self.type = type

    def insert(self):
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
            'type': self.type
            }

"""
Question

"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    difficulty = Column(Integer)
    rating = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.id'))

    def __init__(self, question, answer, category_id, difficulty, rating):
        self.question = question
        self.answer = answer
        self.category_id = category_id
        self.difficulty = difficulty
        self.rating = rating

    def insert(self):
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
            'question': self.question,
            'answer': self.answer,
            'category': self.category_id,
            'difficulty': self.difficulty,
            'rating': self.rating
            }
