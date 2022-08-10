from django.shortcuts import render,redirect
from .models import Room
# Create your views here.

def home_view(request, *args, **kwargs):
    qs = Room.objects.all()
    if qs.exists():
        context = {
            "room_list" : qs
        }
        return render(request, "base/home.html", context, status = 200)

def room_view(request, id, *args, **kwargs):
    qs = Room.objects.filter(id = id)
    if qs.exists():
        context = {
            "room" : qs.first()
        }
        return render(request, "base/room.html", context, status = 200)

def delete_view (request, id, *args, **kwargs ):
    qs = Room.objects.all()
    qs.delete(id= id)
    qs.save()
    context = {
    "room_list" : qs
    }
    redirect("")

def create_room (request, *args, **kwargs):
    
    return render(request,"base/room_form.html", context={"mess":"hello world"})
