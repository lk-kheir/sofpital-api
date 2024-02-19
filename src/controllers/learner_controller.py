from flask import request, Blueprint, jsonify, abort
from src.models.learner_model import Learner
from src.utils import all, get_by_id, to_dict, add, update, token_required, pagination
from src.models.user_model import User
from src.models.post_model import Post, Tag, PostTag
from src.models.offer_model import Offer

# learner controller blueprint to be registered with api blueprint
learner = Blueprint("learner", __name__)


@learner.route('/<learner_id>', methods=["GET"])
@token_required
def get_learner(current_user, learner_id):
    """Get the learner's profile information."""
    """we can just call /api/user/<user_id>"""
    learner = Learner.query.get(learner_id)
    if not learner:
        return jsonify({"error": "Learner not found"}), 404
    dict = to_dict(learner)
    user_id = dict.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(to_dict(user))


@learner.route('/<learner_id>/posts', methods=["GET"])
@token_required
def get_posts_for_learner(current_user, learner_id):
    """Get paginated list of questions asked by the learner."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)

    learner = Learner.query.get(learner_id)
    if not learner:
        return jsonify({"error": "Learner not found"}), 404

    # Paginate the query
    posts = Post.query.filter_by(learner_id=learner_id).paginate(
        page=page, per_page=per_page)

    # Convert paginated results to a list of dictionaries
    list_posts = [to_dict(post) for post in posts.items]

    return jsonify({
        "posts": list_posts,
        "total_pages": posts.pages,
        "total_posts": posts.total
    })


@learner.route('/<learner_id>/posts', methods=["POST"])
@token_required
def creaet_new_post(current_user, learner_id):
    """Ask a question."""
    """insert into post (learner_id, title, description, poste_date, status) values (learner_id, title, description, poste_date, status)"""
    learner = Learner.query.get(learner_id)
    if not learner:
        return jsonify({"error": "Learner not found"}), 404
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    tags = data.get('tags', [])

    # Remove tags from the data so that it doesn't interfere with Post creation
    data.pop('tags', None)

    # Create the post
    post = Post(**data)
    add(post)
    # Associate tags with the post
    for tag_data in tags:
        tag = Tag.query.filter_by(name=tag_data['name']).first()
        if not tag:
            tag = Tag(**tag_data)
            add(tag)
        post_tags = PostTag.query.filter_by(
            post_id=post.id, tag_id=tag.id).first()
        if not post_tags:
            post_tags = PostTag(post_id=post.id, tag_id=tag.id)
            add(post_tags)
        # post.tags.append(tag)
    print(data)

    return jsonify({"status": "success"}), 200


@learner.route('/<learner_id>/posts/<post_id>', methods=["GET"])
@token_required
def get_one_post_by_id(current_user, learner_id, post_id):
    """Get a question by its id."""
    """select * from post where id = post_id"""
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(to_dict(post))


@learner.route('/<learner_id>/posts/received_offers', methods=["GET"])
@token_required
def get_all_recieved_offers(current_user, learner_id):
    """Get all offers for all posts."""
    """select * from offer where post_id in (select id from post where learner_id = learner_id)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)
    learner = Learner.query.get(learner_id)
    if not learner:
        return jsonify({"error": "Learner not found"}), 404
    list_offers = []
    for post in learner.posts:
        if post.offers:
            post_dict = post.to_dict()
            post_dict['offers'] = [offer.to_dict() for offer in post.offers]
            list_offers.append(post_dict)
    res = pagination(list_offers, page, per_page)
    return jsonify({"results": res, "total_results": len(list_offers), "total_pages": len(list_offers)//per_page})


@learner.route('/<learner_id>/posts/<post_id>/recieved_offers', methods = ["GET"])
@token_required
def get_recieved_offers(current_user, learner_id, post_id):
    """Get all offers for a post."""
    """select * from offer where post_id = post_id"""
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    list_offers = []
    for offer in post.offers:
        list_offers.append(to_dict(offer))
    
    print(list_offers)
    return jsonify(list_offers)


@learner.route('/<learner_id>/offers/accepted_offers', methods=["GET"])
@token_required
def get_accepted_offers(current_user, learner_id):
    """Get all accepted offers for all posts."""
    """select * from offer where post_id in (select id from post where learner_id = learner_id) and status = 'accepted'"""
    learner = Learner.query.get(learner_id)
    if not learner:
        return jsonify({"error": "Learner not found"}), 404
    list_offers = []
    for post in learner.posts:
        for offer in post.offers:
            if offer.status == "accepted":
                list_offers.append(offer.to_dict())
    
    return jsonify(list_offers)

@learner.route('/<learner_id>/posts/<post_id>/accept_offer/<offer_id>', methods=["PUT"])
@token_required
def accept_offer(current_user, learner_id, post_id, offer_id):
    """Accept an offer for a post."""
    """make sure to update the offer status to accepted as well"""
    """make sure to update the post status to accepted as well"""
    """make sure to make all other offers for this post rejected"""
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    post.status = "accepted"
    update(post)
    accepted_offer = Offer.query.get(offer_id)
    if not accepted_offer:
        return jsonify({"error": "Offer not found"}), 404
    accepted_offer.status = "accepted"
    update(accepted_offer)
    for other_offer in post.offers:
        if other_offer.status == "pending":
            other_offer.status = "rejected"
            update(other_offer)

    return jsonify({"message": "success"}), 200


@learner.route('/<learner_id>/posts/<post_id>/reject_offer/<offer_id>', methods=["PUT"])
@token_required
def reject_offer(current_user, learner_id, post_id, offer_id):
    """Reject an offer for a post."""
    """make sure to update the offer status to be rejeced"""
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({"error": "Offer not found"}), 404
    offer.status = "rejected"
    update(offer)
    return jsonify({"message": "success"}), 200


@learner.route('/')
def get_all_learner():
    learners = all(Learner)
    # print(learners)
    lst = []
    for val in learners:
        dict = {}
        user_id = val['user_id']
        dict[val['id']] = get_by_id(User, user_id)
        lst.append(dict)
    return jsonify(lst)
