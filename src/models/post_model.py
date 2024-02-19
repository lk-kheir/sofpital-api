from src import db

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    learner_id = db.Column(db.Integer(), db.ForeignKey('learner.id'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    poste_date = db.Column(db.DateTime(),nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    tags = db.relationship('Tag', secondary='post_tag', backref='posts')
    # def __repr__(self):
    #     return f"<Post id={self.id}> learner_id={self.learner_id} title={self.title} 
    #     description={self.description} status={self.status} poste_date={self.poste_date}"


    def to_dict(self):
        return {
            "id": self.id,
            "learner_id": self.learner_id,
            "title": self.title,
            "description": self.description,
            "poste_date": self.poste_date,
            "status": self.status
        }

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class PostTag(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'), nullable=False)
    tag_id = db.Column(db.Integer(), db.ForeignKey('tag.id'), nullable=False)