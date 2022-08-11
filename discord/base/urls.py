from django.contrib import admin
from django.urls import path
from base.views import delete_view, home_view, create_room , room_view, delete_view, update_room
urlpatterns = [
    path('', home_view, name="home"),
    path('<str:pk>/', room_view, name="room"),
    path('update/<str:pk>/', update_room,name="update_room"),
    path('create', create_room, name="create_room"),
    path('delete/<str:pk>', delete_view, name = "delete_room"),
]
