from django.conf.urls import url

from . import views

app_name = 'student'
urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^account$', views.account_view, name='account'),
    url(r'^change_password/$', views.change_password_view, name='change_password'),
    url(r'^class/$', views.class_view, name='class'),
    url(r'^class_schedule/$', views.class_schedule_view, name='class_schedule'),
    url(r'^create/$', views.create_view, name='create'),
    url(r'^forgot_password/$', views.forgot_password_view, name='forgot_password'),
    url(r'^lock_topic/$', views.lock_topic_view, name='lock_topic'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^registerClass/$', views.registerClass_view, name='registerClass'),
    url(r'^registerTutor/$', views.registerTutor_view, name='registerTutor'),
    url(r'^send_reset_link/$', views.send_reset_link_view, name='send_reset_link'),
    url(r'^submit_answer/$', views.submit_answer_view, name='submit_answer'),
    url(r'^tutor/$', views.tutor_view, name='tutor'),
    url(r'^user/$', views.user_view, name='user'),
    url(r'^reset/$', views.reset_view, name='reset'),
    url(r'^update_pw/$', views.update_pw_view, name='update_pw'),
    url(r'^update_personal/$', views.update_personal_view, name='update_personal'),
]