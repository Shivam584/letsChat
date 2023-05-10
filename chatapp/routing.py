from django.urls import path
from . import consumers
websocket_urlpatterns=[
    path('ws/sc/<str:groupName>/',consumers.myChatSync.as_asgi()),
    path('ws/asc/<str:groupName>/',consumers.myChatAsync.as_asgi()),
    path('ws/asc/prv/<str:groupName>/',consumers.PrivateChatConsumer.as_asgi()),
]