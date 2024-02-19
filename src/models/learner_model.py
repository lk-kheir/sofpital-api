from src import db


class Learner(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='learner', uselist=False)
    posts = db.relationship('Post', backref='learner', cascade='all, delete-orphan')    
    offers = db.relationship('Offer', backref='learner', cascade='all, delete-orphan')
