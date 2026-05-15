from django.contrib import admin
from django.urls import path, include
from .views import ChatView

urlpatterns = [
    path('post/', ChatView.as_view(), name='chat'),
]
