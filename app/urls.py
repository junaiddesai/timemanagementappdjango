from django.conf.urls import include, url
import django.contrib.auth.views
import app.forms
import app.views
import app.urls

urlpatterns = [
    url(r'^$', app.views.appHome, name='appHome'),

    url(r'^projects/$', app.views.projects, name='projects'),

    url(r'^create_project/$', app.views.create_project, name='create_project'),

    url(r'^create_job/(?P<project_id>[0-9]+)/$', app.views.create_job, name='create_job'),

    url(r'^project_detail/(?P<project_id>[0-9]+)/$', app.views.project_detail, name='project_detail'),

    url(r'^delete_job/(?P<job_id>[0-9]+)/(?P<project_id>[0-9]+)/$', app.views.delete_job, name='delete_job'),

    url(r'^delete_project/(?P<project_id>[0-9]+)/$', app.views.delete_project, name='delete_project'),
]