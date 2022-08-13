from django.contrib import admin
from django.urls import path
from base.views import (delete_view, home_view, 
create_room , room_view, delete_room, profileUser,
update_room, loginPage,logoutPage,registerPage, deleteMessage)

urlpatterns = [
    path('', home_view, name="home"),
    path('<int:pk>/', room_view, name="room"),
    path('update/<int:pk>/', update_room,name="update_room"),
    path('create/', create_room, name="create_room"),
    path('login/', loginPage, name="login"),
    path('register/' , registerPage, name="register"),
    path('logout/', logoutPage, name="logout"),
    path('delete-message/<int:pk>/', deleteMessage, name="delete-message"),
    path('delete/<int:pk>/', delete_room, name = "delete_room"),
    path('profile/<int:pk>/', profileUser, name = "profile"),

]
