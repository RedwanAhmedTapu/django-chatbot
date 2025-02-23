from django.urls import path
from .views import ChatView, index  # Import the index view

urlpatterns = [
    path('', index, name='index'),  # Serve the chatbot interface
    path('chat/', ChatView.as_view(), name='chat'),
]