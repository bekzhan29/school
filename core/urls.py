from django.conf.urls import url, include
from . import views as core_views
from django.contrib.auth import views as auth_views

app_name = 'core'
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'},
        name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^dashboard/$', core_views.dashboard, name='dashboard'),
    url(r'^$', core_views.dashboard),
]