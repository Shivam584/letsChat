from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Chat(models.Model):
    content=models.CharField(max_length=1000)
    timestamp=models.DateTimeField(auto_now=True)
    group=models.ForeignKey("Grp", on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.SET_DEFAULT,default=-1)

class Grp(models.Model):
    name=models.CharField(max_length=30,unique=True)
