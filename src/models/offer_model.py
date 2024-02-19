from src import db

class Offer(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    tutor_id = db.Column(db.Integer(), db.ForeignKey('tutor.id'), nullable=False)
    learner_id = db.Column(db.Integer(), db.ForeignKey('learner.id'), nullable=False)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    offer_date = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    post = db.relationship('Post', backref='offers')

    # def __repr__(self):
    #     return f"<Offer id={self.id}> tutor_id={self.tutor_id} learner_id={self.learner_id} 
    #     post_id={self.post_id} title={self.title} description={self.description} offer_date={self.offer_date}"


    def to_dict(self):
        return {
            "id": self.id,
            "tutor_id": self.tutor_id,
            "learner_id": self.learner_id,
            "post_id": self.post_id,
            "title": self.title,
            "description": self.description,
            "offer_date": self.offer_date,
            "status": self.status
        }