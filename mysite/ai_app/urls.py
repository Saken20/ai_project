# ai_app/urls.py

from django.urls import path
from . import views

app_name = 'ai_app'

urlpatterns = [
    path('', views.chat_view, name='chat'),  # /chat/
    path('get_response/', views.get_response, name='get_response'),  # /chat/get_response/
    path('get_sessions/', views.get_sessions, name='get_sessions'),  # /chat/get_sessions/
    path('get_session_messages/<int:session_id>/', views.get_session_messages, name='get_session_messages'),  # /chat/get_session_messages/<int:session_id>/
]
