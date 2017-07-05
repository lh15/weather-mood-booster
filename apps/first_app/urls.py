from django.conf.urls import url
from . import views
from views import *          # So we can call functions from our routes!
urlpatterns = [
    url(r'^$', index, name = "index"),
    url(r'^display$', display, name = "display"),          
    url(r'^process_registration$', process_registration, name = 'process_registration'),
    url(r'^process_login$', process_login, name = 'process_login'),
    url(r'^get_weather$', get_weather, name = 'get_weather'),
    url(r'^get_friend_weather$', get_friend_weather, name = 'get_friend_weather'),
    url(r'^process_friend/(?P<id>[^\n]+)/$', process_friend, name = 'process_friend'),
    url(r'^login$', login, name = 'login'),
    url(r'^log_out$', log_out, name = 'log_out'), 
]
