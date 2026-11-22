from django.shortcuts import render
from .crud.read import get_upcoming_events


def event_list(request):
    display_events = [
        {
            "id": str(doc["_id"]),
            "title": doc.get("title") or doc.get("eventName") or "",
            "description": doc.get("description") or "",
            "venue": doc.get("venue") or doc.get("location") or "",
            "status": doc["status"],
        }
        for doc in get_upcoming_events()
    ]

    return render(request, "events/event_list.html", {"events": display_events})