from src import db

class Meeting(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    tutor_id = db.Column(db.Integer(), db.ForeignKey('tutor.id'), nullable=False)
    learner_id = db.Column(db.Integer(), db.ForeignKey('learner.id'), nullable=False)
    offer_id = db.Column(db.Integer(), db.ForeignKey('offer.id'), nullable=False)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    done = db.Column(db.Boolean(), default=False)
    tutor = db.relationship('Tutor', backref='meetings')
    # feedback = db.Column(db.Text(), nullable=True)
    learner = db.relationship('Learner', backref='meetings')
    offer = db.relationship('Offer', backref='meeting')
    post = db.relationship('Post', backref='meeting')

    # def __repr__(self):
    #     return f"<Meeting id={self.id}> tutor_id={self.tutor_id} learner_id={self.learner_id}
    #     offer_id={self.offer_id} post_id={self.post_id} date={self.date} duration={self.duration}"
