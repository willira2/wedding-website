from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
     url(r'^$', views.index, name='index'),
     path('rsvp/', views.rsvp, name='rsvp'),
     url(r'^search/$', views.search, name='search'),
     url(r'^rsvp/find-code/$', views.find_code, name='find_code'),
     url(r'^submit-rsvp/$', views.submit_rsvp, name='submit_rsvp'),
     url(r'^dashboard/$', views.dashboard, name='dashboard'),
     url(r'^thank-you/$', views.thank_you, name='thank_you'),

]

handler404 = 'polls.views.handler404'
