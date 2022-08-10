from django.contrib import admin
from django.urls import path
from base.views import delete_view, home_view, create_room , room_view, delete_view
urlpatterns = [
    path('', home_view),
    path('<int:id>/', room_view, name="room"),
    # path('room/<int:id>/', room_view,name="room"),
    path('create', create_room),
    path('delete/<int:id>', delete_view),
]
