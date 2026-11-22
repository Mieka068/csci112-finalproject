from bson.errors import InvalidId
from django.http import Http404
from django.shortcuts import render

from .crud.read import get_event_by_id, get_upcoming_events


def _display_event(doc):
    return {
        "id": str(doc["_id"]),
        "title": doc.get("title") or doc.get("eventName") or "",
        "description": doc.get("description") or "",
        "venue": doc.get("venue") or doc.get("location") or "",
        "status": doc["status"],
    }


def event_list(request):
    display_events = [_display_event(doc) for doc in get_upcoming_events()]
    return render(request, "events/event_list.html", {"events": display_events})


def event_detail(request, event_id):
    try:
        doc = get_event_by_id(event_id)
    except InvalidId as exc:
        raise Http404("Event not found") from exc

    if doc is None or doc.get("status") != "Upcoming":
        raise Http404("Event not found")

    return render(request, "events/event_detail.html", {"event": _display_event(doc)})
