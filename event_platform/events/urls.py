from django.urls import path
from . import views


urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("create/", views.create_event_view, name='create_event'),
]
