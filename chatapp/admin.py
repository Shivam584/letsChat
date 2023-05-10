from django.contrib import admin
from .models import *
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display=['id','content','timestamp','group']
@admin.register(Grp)
class GrpAdmin(admin.ModelAdmin):
    list_display=['id','name']
class privateRoomAdmin(admin.ModelAdmin):
    list_display=['id','sender','reciever','content','chatcode','timestamp']