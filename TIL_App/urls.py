from django.conf.urls import url
from . import views

app_name = 'TIL'

urlpatterns = [
    url(r'^$', views.login_page, name='login'),
    url(r'TIL_welcome/$', views.welcome_page, name='welcome'),
    url(r'^TIL_smthng_new/(?P<pk>\d+)/$', views.tell_me, name='tell_me'),
    url(r'^TIL_about/$', views.about_page, name='about'),
]