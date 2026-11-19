from database.db_collections import participants, organizers, users
from bson import ObjectId

def delete_participant(participant_id):
    return participants.delete_one({
        "_id": ObjectId(participant_id)
    })

def delete_organizer(organizer_id):
    return organizers.delete_one({
        "_id": ObjectId(organizer_id)
    })

def delete_user(user_id):
    return users.delete_one({
        "_id": ObjectId(user_id)
    })