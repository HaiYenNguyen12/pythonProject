from django.shortcuts import render,redirect
from .models import Room,Topic
from .forms import RoomForm
# Create your views here.

def home_view(request, *args, **kwargs):
    q = request.GET.get("q")
    if q != None:
        qs = Room.objects.filter(topic__name__icontains=q)
    else:
        qs = Room.objects.all()
    qs_topic = Topic.objects.all()
    if qs.exists():
        context = {
            "room_list" : qs,
            "topics" : qs_topic
        }
        return render(request, "base/home.html", context, status = 200)

def room_view(request, pk, *args, **kwargs):
    qs = Room.objects.filter(id = pk)
    if qs.exists():
        context = {
            "room" : qs.first()
        }
        return render(request, "base/room.html", context, status = 200)

def delete_view (request, pk, *args, **kwargs ):
    qs = Room.objects.all()
    qs.delete(id = pk)
    qs.save()
    context = {
    "room_list" : qs
    }
    return redirect("home")

def create_room (request, *args, **kwargs):
    form  = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {
        "form" : form
    }
    
    return render(request,"base/room_form.html", context)


def update_room (request, pk, *args, **kwargs ):
    qs = Room.objects.get(id = pk)
    form  = RoomForm(instance=qs)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=qs)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {
        "form" : form
    }
    
    return render(request,"base/room_form.html", context)


    
def delete_view(request, pk, *args, **kwargs):
    obj = Room.objects.get(id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("home")

    return render(request,"base/delete.html", context={"room" : obj})
