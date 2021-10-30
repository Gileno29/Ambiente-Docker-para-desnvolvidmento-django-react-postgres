from django.conf.urls import url
from django.urls import path, include
from .views import MusicList

   

urlpatterns =[
    path('api/', MusicList.as_view(), name='music'),
]
