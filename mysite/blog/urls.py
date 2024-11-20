from django.urls import path, include
from django.urls import path
from blog import views
from django.urls import path


app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('test/', views.test, name='test'),
    path('send-review/', views.send_review, name='send_review'),
]
