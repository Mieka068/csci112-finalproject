from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .crud.create import create_event
from .crud.read import (
    get_all_events,
    get_event_by_id,
    get_events_by_organization
)
from .crud.update import update_event
from .form_choices import STATUSES, TYPES
from datetime import datetime
from bson import ObjectId


def event_list(request):
    event_list = get_all_events()

    return render(
        request,
        "events/event_list.html",
        {"events": event_list}
    )

def create_event_view(request):
    if not request.session.get('user_id'):
        return redirect('login')

    if request.session.get('role') != 'organizer':
        messages.error(request, 'Only organizers can create events.')
        return redirect('home')

    if request.method == 'POST':
        start_time = timezone.make_aware(datetime.strptime(
            request.POST.get('startTime'),
            '%Y-%m-%dT%H:%M'
        ))
        end_time = timezone.make_aware(datetime.strptime(
            request.POST.get('endTime'),
            '%Y-%m-%dT%H:%M'
        ))

        if start_time < timezone.localtime():
            messages.error(request, 'Start time cannot be in the past.')
        elif end_time < start_time:
            messages.error(request, 'End time cannot be earlier than start time.')
        else:
            event = {
                'eventName': request.POST.get('title', '').strip(),
                'description': request.POST.get('description', '').strip(),
                'startTime': start_time,
                'endTime': end_time,
                'location': request.POST.get('venue', '').strip(),
                'eventType': request.POST.get('type', '').strip(),
                'maxParticipants': int(request.POST.get('maxParticipants')),
                'currentParticipants': 0,
                'openToAll': request.POST.get('openToAll') == 'on',
                'organizationID': ObjectId(request.session.get('profile_id')),
                'status': 'Upcoming'
            }

            create_event(event)
            messages.success(request, 'Event created successfully.')
            return redirect('event_list')

    return render(request, 'events/create_event.html', {
        'statuses': STATUSES,
        'types': TYPES
    })

def edit_event_view(request, event_id):
    if not request.session.get('user_id'):
            return redirect('login')
    
    event = get_event_by_id(event_id)
    if event['organizationID'] != ObjectId(request.session.get('profile_id')):
        messages.error(request, 'You cannot edit this event.')
        return redirect('event_list')

    if request.method == 'POST':
        start_time = timezone.make_aware(datetime.strptime(
            request.POST.get('startTime'),
            '%Y-%m-%dT%H:%M'
        ))
        end_time = timezone.make_aware(datetime.strptime(
            request.POST.get('endTime'),
            '%Y-%m-%dT%H:%M'
        ))

        if start_time < timezone.localtime():
            messages.error(request, 'Start time cannot be in the past.')
        elif end_time < start_time:
            messages.error(request, 'End time cannot be earlier than start time.')
        else:
            updated_data = {
                'eventName': request.POST.get('title', '').strip(),
                'description': request.POST.get('description', '').strip(),
                'startTime': start_time,
                'endTime': end_time,
                'location': request.POST.get('venue', '').strip(),
                'eventType': request.POST.get('type', '').strip(),
                'maxParticipants': int(request.POST.get('maxParticipants')),
                'openToAll': request.POST.get('openToAll') == 'on',
                'status': request.POST.get('status')
            }

            update_event(event_id, updated_data)
            messages.success(request, 'Event updated successfully.')
            return redirect('event_list')

    return render(request, 'events/edit_event.html', {
        'event': event,
        'types': TYPES,
        'statuses': STATUSES,
        'start_time': timezone.make_aware(event['startTime']).strftime('%Y-%m-%dT%H:%M'),
        'end_time': timezone.make_aware(event['endTime']).strftime('%Y-%m-%dT%H:%M'),
        'event_id': event_id
    })

def org_event_list_view(request):
    if not request.session.get('user_id'):
        return redirect('login')

    if request.session.get('role') != 'organizer':
        messages.error(request, 'Only organizers can view this page.')
        return redirect('home')

    org_events = get_events_by_organization(request.session.get('profile_id'))
    for event in org_events:
        event['event_id'] = str(event['_id'])
   
    return render(request, 'events/org_event_list.html', {
        'events': org_events
    })

def event_detail_view(request, event_id):
    event = get_event_by_id(event_id)
    return render(request, 'events/event_detail.html', {
        'event': event,
        'event_id': event_id
    })
