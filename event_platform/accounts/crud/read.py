from database.db_collections import participants, organizers, users
from bson import ObjectId

# Participants
def get_all_participants():
    return list(participants.find())

def get_participant_by_id(participant_id):
    return participants.find_one({
        "_id": ObjectId(participant_id)
    })

def get_participant_by_student_id(id_number):
    return participants.find_one({
        "idNumber": id_number
    })

def get_participant_by_email(email):
    return participants.find_one({
        "email": email
    })

# Organizers
def get_all_organizers():
    return list(organizers.find())

def get_organizer_by_id(organizer_id):
    return organizers.find_one({
        "_id": ObjectId(organizer_id)
    })

def get_organizer_by_name(organization_name):
    return organizers.find_one({
        "organizationName": organization_name
    })

# Users
def get_all_users():
    return list(users.find())

def get_user_by_id(user_id):
    return users.find_one({
        "_id": ObjectId(user_id)
    })


def get_user_by_email(email):
    return users.find_one({
        "email": email
    })