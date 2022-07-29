from django.contrib import admin
from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('' , views.home , name='home'),
   
    path('doctor' , views.doctor , name='doctor'),
    path('viewevent' , views.viewevent , name='viewevent    '),
    path('confirm' , views.confirm , name='confirm'),
    path('bookform/<str:pk>/' , views.bookform , name='bookform'),
    path('blog/<str:pk>/',views.blog, name='blog'),
    path('register/' , views.register , name='register'),
    path('log/' , views.log , name='log'),
    path('about/' , views.about , name='about'),
    path('create_topic/' , views.create_topic , name='create_topic'),
    path('create_blog/' , views.create_blog , name='create_blog'),
    path('logout_form/' , views.logout_form , name='logout_form'),

]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)