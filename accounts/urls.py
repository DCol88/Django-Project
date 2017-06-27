from django.conf.urls import url
from .views import logout, profile

urlpatterns = [
    url(r'^logout/$', logout, name='logout'),
    
]