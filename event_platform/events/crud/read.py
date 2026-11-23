from database.db_collections import events, registrations, participants
from bson import ObjectId

def get_all_events():
    return list(events.find({
        "status": { "$ne": "Cancelled" }
    }))

def get_event_by_id(event_id):
    return events.find_one({
        "_id": ObjectId(event_id)
    })

def get_events_by_organization(org_id):
    return list(events.find({
        "organizationID": ObjectId(org_id)
    }))

def get_event_participants(event_id):
    registered = list(registrations.find({
        "eventID": ObjectId(event_id)
    }))

    participant_ids = [
        registration['participantID']
        for registration in registered
    ]

    return list(participants.find({
        "_id": { "$in": participant_ids }
    }))
