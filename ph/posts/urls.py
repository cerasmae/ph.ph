from django.conf.urls import url
from django.views.generic.edit import CreateView

from . import views
from . import forms

urlpatterns = [
	url(r'^signup/', views.signup_view, name='signup'),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^user-profile/(?P<user_id>\d+)/(?P<user_username>[\w\-]+)/$', views.user_profile, name='user-profile'),
    url(r'^post/(?P<post_id>\d+)/$', views.post_detail, name='post-detail'),
    url(r'^post/(?P<post_id>\d+)/(?P<slug>[-\w\d]+)/$', views.post_detail, name='post-detail'),


    url(r'^create/$', views.ckeditor_form_view, name='ckeditor-form'),
]