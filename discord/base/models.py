from turtle import mode
from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class Topic (models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField(blank=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[0:5]