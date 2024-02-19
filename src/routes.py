from flask import Blueprint, jsonify, request
from src.controllers.user_controller import user  
from src.controllers.auth_controller import auth 
from src.controllers.learner_controller import learner
from src.controllers.tutor_controller import tutor
from src.controllers.meeting_controller import meeting
from src.models.user_model import User
from src.models.learner_model import Learner
from src.models.tutor_model import Tutor
from src.models.meeting_model import Meeting
from src.models.post_model import Post
from src.models.offer_model import Offer
from src.utils import all


# main blueprint to be registered with application
api = Blueprint('api', __name__)

    # register user with api blueprint
api.register_blueprint(user, url_prefix="/user")
api.register_blueprint(auth, url_prefix="/auth")
api.register_blueprint(learner, url_prefix="/learner")
api.register_blueprint(tutor, url_prefix="/tutor")
api.register_blueprint(meeting, url_prefix="/meeting")


@api.route('/welcome', methods = ["GET"])
def welcome():
    return jsonify({"message": "Welcome to the API"})

@api.route('/search/posts', methods = ["GET"])
def search_posts(query):
    query = request.args.get('query')
    # search for description and title
    posts = all(Post)
    matched_posts = [post for post in posts if query.lower() in post.title.lower() or query.lower() in post.description.lower()]
    return jsonify(matched_posts)

@api.route('/search/', methods = ["GET"])
def search():
    # Perform the search logic here
    models = {
        "users": all(User),
        "learners": all(Learner),
        "tutors": all(Tutor),
        "meetings": all(Meeting),
        "posts": all(Post),
        "offers": all(Offer)
    }
    query = request.args.get('query')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    results = {}

    for model, data in models.items():
        matched_items = [item for item in data if query.lower() in str(item).lower()]
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_items = matched_items[start_index:end_index]
        if paginated_items:
            results[model] = paginated_items
    # Return the results as JSON
    return jsonify({
        "results": results,
        "pagination": {
            "page": page,
            "per_page": per_page,
            # "total_pages": max(1, len(matched_items) // per_page),
            # "total_items": len(matched_items)
        }})