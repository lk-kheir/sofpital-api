from flask import request, Response, json, Blueprint, jsonify, abort
from sqlalchemy import exists
from src import db
from src.models.tutor_model import Tutor, TutorSubject, Subject
from src.models.offer_model import Offer
from src.models.post_model import Post, PostTag, Tag
from src.models.user_model import User
from src.utils import all, get_by_id, to_dict, add, token_required

# tutor controller blueprint to be registered with api blueprint
tutor = Blueprint("tutor", __name__)

@tutor.route('/<tutor_id>', methods = ["GET"])
@token_required
def get_tutor(current_user,tutor_id):
    """Get the tutor's profile information."""
    """we can just call /api/user/<user_id>"""
    tutor = Tutor.query.get(tutor_id)
    if not tutor:
        return jsonify({"error": "Tutor not found"}), 404
    
    user_id = tutor.user_id
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return {
        "tutor": to_dict(tutor),
        "user": to_dict(user)
    } 


@tutor.route('/<tutor_id>/recommended_posts', methods = ["GET"])
@token_required
def get_posts_for_tutor(current_user, tutor_id):
    """return the last 10 recent posts by any learner."""
    tutor = Tutor.query.get_or_404(tutor_id)

    subjects = tutor.subjects
    # recommended_posts = (
    #     Post.query
    #     .select_from(Post)  # Specify the FROM clause first
    #     .join(PostTag)
    #     .join(Tag)
    #     .join(TutorSubject, TutorSubject.subject_id.in_([subject.id for subject in subjects]))
    #     .all()
    # )

    # print(recommended_posts)
    posts_with_offers = (
        Post.query
        .join(Offer, Offer.post_id == Post.id)
        .filter(Offer.tutor_id == tutor_id)
        .all()
    )
    recommended_posts = (
        Post.query
        .select_from(Post)
        .join(PostTag)
        .join(Tag)
        .join(TutorSubject, TutorSubject.subject_id.in_([subject.id for subject in tutor.subjects]))
        .filter(~Post.id.in_([post.id for post in posts_with_offers]))  # Exclude posts with offers
        .all()
    )
    # Get other posts (excluding the recommended and those with offers)
    other_posts = Post.query.filter(
        ~Post.id.in_([post.id for post in recommended_posts]),
        ~Post.id.in_([post.id for post in posts_with_offers])
    ).all()

    all_posts = recommended_posts + other_posts
    formatted_posts = [post.to_dict() for post in all_posts]
    # print(formatted_posts)
    return jsonify({"recommended_posts": formatted_posts})

    


@tutor.route('/<tutor_id>/offers', methods = ["GET"])
@token_required
def get_offers_for_tutor(current_user, tutor_id):
    """Get all offers offered by the tutor."""
    offer_list = []
    tutor = Tutor.query.get(tutor_id)
    if not tutor:
        return jsonify({"error": "Tutor not found"}), 404
    for offer in tutor.offers:
        offer_list.append(to_dict(offer))
    return jsonify(offer_list)


@tutor.route('/<tutor_id>/offers/post/<post_id>', methods = ["POST"])
@token_required
def creat_new_offer(current_user, tutor_id, post_id):
    """
        Make an offer.
        we make sure that the tutor exists and the post exists.
        we make sure that tutor can make only one offer for a post.
    """
    tutor = Tutor.query.get(tutor_id)
    if not tutor:
        return jsonify({"error": "Tutor not found"}), 404
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    # check if the post exists
    stmt = exists().where(Offer.post_id == post_id, Offer.tutor_id == tutor_id)
    if db.session.query(stmt).scalar():
        return jsonify({"error": "Tutor can only make one offer for a post"}), 400
    
    data = request.get_json()
    print(data)
    offer = Offer(**data)
    offer.tutor_id = tutor_id
    offer.post_id = post_id
    add(offer)
    return jsonify({"status": "success"}), 200


@tutor.route('/<tutor_id>/offers/<offer_id>', methods = ["GET"])
@token_required
def get_one_offer_by_id(current_user, tutor_id, offer_id):
    offer = Offer.query.filter_by(id=offer_id, tutor_id=tutor_id).first()
    if offer is None:
        return jsonify({'error': 'Offer not found or offer does not belong to tutor'}), 404
    
    return jsonify(to_dict(offer)), 200
