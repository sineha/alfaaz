from django.urls import path,include
from . import views

urlpatterns = [ 
    path('',views.home,name='home'),
    path('start_Recording',views.start_Recording,name='start_Recording'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('stop', views.stop, name='stop'),
    path('translate', views.translate, name='translate'),
]
