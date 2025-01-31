from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import foreign

db = SQLAlchemy()




class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    linked_student_id = db.Column(db.Integer, db.ForeignKey('users.linked_student_id'))
    achievements = db.relationship('StudentAchievement', back_populates='student', foreign_keys='[StudentAchievement.linked_student_id]')



class StudentAchievement(db.Model):
    __tablename__ = 'student_achievements'
    id = db.Column(db.Integer, primary_key=True)
    linked_student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    school_name = db.Column(db.String(100), nullable=False)
    achievement = db.Column(db.Text, nullable=False)
    student = db.relationship('User', back_populates='achievements', foreign_keys=[linked_student_id])


