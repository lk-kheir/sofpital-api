from flask import request, Response, json, Blueprint, jsonify, abort
from src.models.user_model import User
from src.models.learner_model import Learner
from src.models.tutor_model import Tutor
import base64
from src import db
from src.utils import get_by_id, all, update, add, delete, to_dict, token_required

# user controller blueprint to be registered with api blueprint
user = Blueprint("user", __name__)


# route for Get the user's profile information.
@user.route('/<user_id>')
@token_required
def get_user(current_user, user_id):
    user = User.query.get(user_id)
    
    if not user:
        abort(404)
    learner = Learner.query.filter_by(user_id=user_id).first()
    tutor = Tutor.query.filter_by(user_id=user_id).first()

    if learner:
        user.learner_id = learner.id
    if tutor:
        user.tutor_id = tutor.id

    return jsonify(to_dict(user))


#profile
@user.route('/profile')
@token_required
def get_user_profile(current_user):
    user_id = current_user.id

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role == 'learner':
        learner_profile = Learner.query.filter_by(user_id=user.id).first()

        if learner_profile:
            user_dict = to_dict(user)
            learner_dict = to_dict(learner_profile)
            posts = learner_profile.posts
            meetings = learner_profile.meetings
            posts_lst = [post.to_dict() for post in posts]
            meetings_lst = [to_dict(meeting) for meeting in meetings]
            learner_dict['posts'] = posts_lst
            learner_dict['meetings'] = meetings_lst

            # Merge learner dictionary into user dictionary
            learner_dict.update(user_dict)

            # Return the merged dictionary under the 'learner_profile' key
            return jsonify({'learner_profile': learner_dict})
        else:
            return jsonify({'error': 'Learner profile not found'}), 404

    elif user.role == 'tutor':
        tutor_profile = Tutor.query.filter_by(user_id=user.id).first()
        if tutor_profile:
            user_dict = to_dict(user)
            tutor_dict = to_dict(tutor_profile)
            offers = tutor_profile.offers
            meetings = tutor_profile.meetings
            offers_lst = [offer.to_dict() for offer in offers]
            meetings_lst = [to_dict(meeting) for meeting in meetings]
            tutor_dict['offers'] = offers_lst
            tutor_dict['meetings'] = meetings_lst

            # Merge tutor dictionary into user dictionary
            tutor_dict.update(user_dict)

            # Return the merged dictionary under the 'tutor_profile' key
            return jsonify({'tutor_profile': tutor_dict})
        else:
            return jsonify({'error': 'Tutor profile not found'}), 404

    else:
        return jsonify({'error': 'Invalid user role'}), 400
    # user info + tutor info + learner info
    # history of all posts if learner
    # history of all offers if tutor
    # history of all meetings

@user.route('/', methods = ["POST"])
def create_user():
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    user = User(**data)
    add(user)
    return jsonify({'message': 'User created successfully'}), 200

# when delete a user, we need to delete all the posts and offers that the user created
@user.route('/<user_id>', methods = ["DELETE"])
@token_required
def delete_user(current_user, user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    delete(user)
    return jsonify({'message': 'User deleted successfully'}), 200



# route for Update the user's profile information.
@user.route('/<user_id>', methods = ["PUT"])
def update_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, val in data.items():
        if key == 'profile_picture_blob' and val is not None:
            # Convert base64-encoded string to bytes
            val = base64.b64decode(val)
        setattr(user, key, val)
    update(user)
    return jsonify({'message': 'User updated successfully'}), 200
