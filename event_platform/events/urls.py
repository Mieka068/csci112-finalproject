from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view),
    path("register/", views.register_view),
    path("", views.event_list, name="event_list"),
]