from channels.consumer import AsyncConsumer,SyncConsumer,StopConsumer
from time import sleep
from .models import *
from channels_redis.core import RedisChannelLayer
from channels.db import database_sync_to_async
import asyncio,json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
from google.transliteration import transliterate_text
class myChatSync(SyncConsumer):
    def websocket_connect(self,event):
        print('connect established',event) 
        self.send({'type': 'websocket.accept'})
        print('channel layer .....',self.channel_layer) 
        print('channel name .....',self.channel_name) 
        async_to_sync(self.channel_layer.group_add)('prog',self.channel_name)
    def websocket_receive(self, event):
        print('message recieved :  ', event['text'])
        async_to_sync(self.channel_layer.group_send)('prog',
            {
                'type':'chat.message',
                'message': event['text']
            }
        )
        
    def websocket_disconnect(self,event):
        print('connect disconnect')
        print('channel layer .....', self.channel_layer)
        print('channel name .....', self.channel_name)
        #discard a channel 
        async_to_sync(self.channel_layer.group_discard)('prog', self.channel_name)
        raise StopConsumer()
    
    def chat_message(self,event):
        print('envent.. ', event)
        self.send({
            'type': 'websocket.send',
            'text' : event['message']
        })

class myChatAsync(AsyncConsumer):
    async def websocket_connect(self,event):
        print('connect established',event) 
        await self.send({'type': 'websocket.accept'})
        print('channel layer .....',self.channel_layer) 
        print('channel name .....',self.channel_name) 
        # to add channel to new /existing group
        grp_name=self.scope['url_route']['kwargs']['groupName']
        print('grp name: ',self.scope['url_route']['kwargs']['groupName'])
        await self.channel_layer.group_add(grp_name,self.channel_name)


    async def websocket_receive(self, event):
        grp_name=self.scope['url_route']['kwargs']['groupName']
        print('message recieved :  ', event['text'])
        user=self.scope['user']
        print(user)
        if user.is_authenticated:
            pyobj = json.loads(event['text'])
            print(pyobj)
            pyobj['username']=user.username
            grpobj= await sync_to_async(Grp.objects.get)(name=grp_name)
            chatobj=Chat(content=pyobj['msg'],group=grpobj,user=user)
            pyobj['msg']=transliterate_text(pyobj['msg'], lang_code=pyobj['lang'])
            print(pyobj['msg'])
            await sync_to_async(chatobj.save)()
            await self.channel_layer.group_send(grp_name,
                {
                    'type':'chat.message',
                   'message': json.dumps(pyobj)
                }
            )
        else:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'msg': 'login required'})
            })

    async def chat_message(self,event):
            print('envent.. ', event)
            await self.send({
                'type': 'websocket.send',
                'text' : event['message']
            })

    

    async def websocket_disconnect(self,event):
        grp_name=self.scope['url_route']['kwargs']['groupName']
        print('connect disconnect')
        print('channel layer .....', self.channel_layer)
        print('channel name .....', self.channel_name)
        #discard a channel 
        await self.channel_layer.group_discard(grp_name, self.channel_name)
        raise StopConsumer()
    

lent=0
class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group if there are less than 2 members
        grp_name=self.scope['url_route']['kwargs']['groupName']
        global lent
        lent=lent+1
        print(grp_name,lent)
        if lent<=2:
            await self.channel_layer.group_add(
                grp_name,
                self.channel_name
            )
            
            await self.accept()
        else:
            await self.close()

    async def disconnect(self,close_code):
        grp_name=self.scope['url_route']['kwargs']['groupName']
        global lent
        lent=lent-1
        print('connect disconnect',lent)
        print('channel layer .....', self.channel_layer)
        print('channel name .....', self.channel_name)
        #discard a channel 
        await self.channel_layer.group_discard(grp_name, self.channel_name)
        raise StopConsumer()


    async def receive(self, text_data=None):
        grp_name=self.scope['url_route']['kwargs']['groupName']
        print(type(text_data))
        print('message recieved :  ', text_data)
        user=self.scope['user']
        print(user)
        if user.is_authenticated:
            pyobj = json.loads(text_data)
            print(pyobj)
            pyobj['username']=user.username
            grpobj= await sync_to_async(Grp.objects.get)(name=grp_name)
            chatobj=Chat(content=pyobj['msg'],group=grpobj,user=user)
            pyobj['msg']=transliterate_text(pyobj['msg'], lang_code=pyobj['lang'])
            await sync_to_async(chatobj.save)()
            await self.channel_layer.group_send(grp_name,
                {
                    'type':'chat.message',
                    'message': json.dumps(pyobj)
                }
            )
        else:
            await self.send(text_data="login required")

    async def chat_message(self,event):
            print('event.. ', event)
            await self.send(text_data=event['message'])






# class myChatAsync(AsyncConsumer):
#     async def websocket_connect(self,event):
#         await self.send({'type': 'websocket.accept'})
#         print('connect established')
#     async def websocket_receive(self, event):
#         print('message recieved', event['text'])
#         for x in range(10):
#             await self.send({
#                 'type': 'websocket.send',
#                 'text': json.dumps({'count': x})
#             })
#             await asyncio.sleep(1)
#     async def websocket_disconnect(self,event):
#         print('connect disconnect',event)
#         raise StopConsumer()