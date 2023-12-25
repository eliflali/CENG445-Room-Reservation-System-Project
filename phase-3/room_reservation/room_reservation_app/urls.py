# room_reservation_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),  # Assuming you have an index view
    #path('command/', views.command_view, name='command_view'),
    #path('map/', views.map_view, name='map_view'), #for SVG map
    path('', views.combined_view, name='combined_view'),
    # You can add more URL patterns here
]

