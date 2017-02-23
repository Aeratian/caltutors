from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^team/$', views.team_view, name='team'),
    url(r'^classes/$', views.classes_view, name='classes'),
    url(r'^tutors/$', views.tutors_view, name='tutors'),
    url(r'^photo/$', views.photo_view, name='photo'),
    url(r'^contact/$', views.contact_view, name='contact'),
    url(r'^contact_submit/$', views.contact_submit_view, name='contact_submit'),
    url(r'^team_member/$', views.team_member_view, name='team_member'),
]