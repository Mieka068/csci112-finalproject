from database.db_collections import events
from bson import ObjectId


def update_event(event_id, updated_data):
    return events.update_one(
        { "_id": ObjectId(event_id) },
        { "$set": updated_data }
    )
