from flask import request, Response, json, Blueprint, jsonify, abort
from src.models.meeting_model import Meeting
from src.models.learner_model import Learner
from src.models.tutor_model import Tutor
from src.utils import all, get_by_id, to_dict, add, update, token_required, pagination

# meeting controller blueprint to be registered with api blueprint

meeting = Blueprint("meeting", __name__)

@meeting.route('/')
@token_required
def get_all_meetings(current_user):
    """get all meetings"""
    meetings = all(Meeting)
    list_meetings = [to_dict(meeting) for meeting in meetings]
    return jsonify(list_meetings)

@meeting.route('/<meeting_id>' , methods = ["GET"])
@token_required
def get_meeting_by_id(current_user,meeting_id):
    """get all information about a meeting"""
    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404
    return jsonify(to_dict(meeting))


@meeting.route('/learner/<learner_id>', methods = ["GET"])
@token_required
def get_meetings_for_learner(current_user, learner_id):
    """get all meetings for a learner"""
    learner = Learner.query.get(learner_id)
    page = request.args.get('page', 1, type=int)

    print(request.args)
    per_page = request.args.get('per_page', 8, type=int)
    if not learner:
        return jsonify({"error": "Learner not found"}), 404
    list_meetings = []
    for meeting in learner.meetings:
        list_meetings.append(to_dict(meeting))
    res = pagination(list_meetings, page, per_page)
    return jsonify({"meetings": res, "total_results": len(list_meetings), "total_pages": len(list_meetings)//per_page})

@meeting.route('/learner/<learner_id>/accepted_offers', methods = ["GET"])
@token_required
def get_accepted_meetings_for_learner(current_user, learner_id):
    """get all accepted meetings for a learner"""
    learner = Learner.query.get(learner_id)
    if not learner:
        return jsonify({"error": "Learner not found"}), 404
    list_offers = []
    for offer in learner.offers:
        if offer.status == "accepted" and not offer.meeting:
            list_offers.append(to_dict(offer))
    return jsonify(list_offers)

@meeting.route('/tutor/<tutor_id>', methods = ["GET"])
@token_required
def get_meetings_for_tutor(current_user, tutor_id):
    """get all meetings for a tutor"""
    tutor = Tutor.query.get(tutor_id)
    if not tutor:
        return jsonify({"error": "Tutor not found"}), 404
    list_meetings = []
    for meeting in tutor.meetings:
        list_meetings.append(to_dict(meeting))
    return jsonify(list_meetings)
    
@meeting.route('/', methods = ["POST"])
@token_required
def create_new_meeting(current_user):
    """create a new meeting"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    print(data)
    meeting = Meeting(**data)
    add(meeting)
    return jsonify({"status": "success"}), 200
