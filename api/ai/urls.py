from django.urls import path

from .views import openai_chat  # Importe a view que você criou

urlpatterns = [
    path("chat/", openai_chat, name="chat-openai"),  # Define a URL para a view
]
