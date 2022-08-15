import imp
from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Message, Room,Topic
from .forms import RoomForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

def home_view(request, *args, **kwargs):
    q = request.GET.get("q")
    if q != None:
        qs = Room.objects.filter(Q(topic__name__icontains=q)
         | Q(name__icontains= q) 
         | Q(desc__icontains = q))
        room_messages = Message.objects.filter(Q(room__topic__name__icontains= q))
        
    else:
        qs = Room.objects.all()
        room_messages = Message.objects.all().order_by('-created')
    qs_topic = Topic.objects.all()
   
    if qs.exists():
        context = {
            "room_list" : qs,
            "topics" : qs_topic,
            "room_count" : qs.count(),
            "room_messages" : room_messages
        }
    else:
        return render(request, "base/home.html", context={}, status = 200)
    return render(request, "base/home.html", context, status = 200)

def room_view(request, pk, *args, **kwargs):
    room = Room.objects.get(id = pk)
    messages_room = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            content = request.POST.get("content")
        )
        room.participants.add(request.user)
        return redirect("room", pk =  room.id)
        
    if room != None:
        context = {
            "room" : room,
            "messages_room" : messages_room,
            "participants" : participants 
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



@login_required(login_url='/room/login/')
def create_room (request, *args, **kwargs):
    form  = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic').upper()
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get("name"),
            desc = request.POST.get("desc"),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     temp_room = form.save(commit=False)
        #     temp_room.host = request.user
        #     temp_room.save()
        return redirect("home")

    context = {
        "form" : form, 
        "topics" : topics
    }
    
    return render(request,"base/room_form.html", context)



@login_required(login_url='/room/login/')
def update_room (request, pk, *args, **kwargs ):
    qs = Room.objects.get(id = pk)
    form  = RoomForm(instance=qs)

    topics = Topic.objects.all()
    if request.method == 'POST':    
        topic_name = request.POST.get('topic').upper()
        topic, created = Topic.objects.get_or_create(name=topic_name)
        qs.topic= topic
        qs.name = request.POST.get("name")
        qs.desc = request.POST.get("desc")
        qs.save()
        return redirect("home")

    context = {
        "form" : form,
        "topics" : topics,
        "room" : qs
    }
    
    return render(request,"base/room_form.html", context)



@login_required(login_url='/room/login/')    
def delete_room(request, pk, *args, **kwargs):
    obj = Room.objects.get(id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("home")

    return render(request,"base/delete.html", context={"room": obj})

def loginPage(request, *args, **kwargs):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'The user does not exists')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
             messages.error(request, 'Invalid login')

        
    

    return  render(request, "base/login_register.html", context={"page":page})



def registerPage(request, *args, **kwargs):
    form  = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
    return render(request,'base/login_register.html', {"form": form})
    



def logoutPage (request, *args, **kwargs):
    logout(request)
    return redirect("home")

@login_required(login_url='/room/login/')    
def deleteMessage(request, pk,  *args, **kwargs):
    page = 'del_mess'

    obj = Message.objects.get(id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("room", pk =  obj.room.id)
    context = {
        "obj" : obj,
        "page" : page
    }
    return render(request,"base/delete.html", context=context)


def profileUser(request, pk , *args, **kwargs):
    user = User.objects.get(id=pk)
    qs_topic = Topic.objects.all()
    room_list = user.room_set.all()
    room_messages = user.message_set.all()
    context={
        "user": user,
        "room_list": room_list, 
        "room_count" : room_list.count(),
        "room_messages" : room_messages,
        "topics" : qs_topic,

        }
    return render(request, "base/profile.html",context )

@login_required(login_url='/room/login/')
def updateUser(request, *args, **kwargs):
    user =request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    return render(request, "base/edit-user.html", context={'form':form})


def topicPage(request, *args, **kwargs):
    topics = Topic.objects.all()
    return render(request, "base/topics.html", context={"topics" : topics})