from django.conf.urls import url, include
from . import views as core_views
from django.contrib.auth import views as auth_views

app_name = 'core'
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'},
        name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^dashboard/$', core_views.dashboard, name='dashboard'),
    # TODO(aibeksmagulov): can we actually give the same names to urls, even if their params differ?
    url(r'^group/(?P<pk>[0-9]+)/$', core_views.group, name='group_pk'),
    url(r'^group/(?P<pk>[0-9]+)/day/(?P<day>[0-9]+)/$', core_views.group, name='group_pk_day'),
    url(r'^attend/$', core_views.attend, name='attend'),
    url(r'^$', core_views.dashboard),
]