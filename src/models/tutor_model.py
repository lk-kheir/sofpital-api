from src import db
from src import app


class Tutor(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    biography = db.Column(db.Text(), nullable=True)
    available = db.Column(db.Boolean(), default=True)
    user = db.relationship('User', back_populates='tutor', uselist=False)
    offers = db.relationship('Offer', backref='tutor', cascade='all, delete-orphan')
    subjects = db.relationship('Subject', secondary='tutor_subject', backref='tutors')

class Subject(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class TutorSubject(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    tutor_id = db.Column(db.Integer(), db.ForeignKey('tutor.id'), nullable=False)
    subject_id = db.Column(db.Integer(), db.ForeignKey('subject.id'), nullable=False)