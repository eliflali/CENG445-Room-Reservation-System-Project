# room_reservation_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Assuming you have an index view
    path('command/', views.command_view, name='command_view'),
    # You can add more URL patterns here
]

