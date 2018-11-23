from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
     path('', views.IndexView.as_view(), name='index'),
     path('rsvp/', views.RsvpView.as_view(), name='rsvp'),
]
