from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.logout, name='edit'),
    path('register/', views.register, name='register'),
    path('register/participant/', views.participant_register, name='participant_register'),
    path('register/organizer/', views.organizer_register, name='organizer_register'),
]