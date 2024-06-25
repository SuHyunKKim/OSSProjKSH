import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import ChatRoom, AppUser, Chat  # 여기에 모델 임포트

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Received message: {text_data}")
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'initial_load':
            chatRoomId = data.get('chatRoomId')
            if chatRoomId:
                await self.load_initial_messages(chatRoomId)
        else:
            CHistoryID = data.get('CHistoryID')
            senderID = data.get('senderID')
            receiverID = data.get('receiverID')
            content = data.get('content')

            if CHistoryID and senderID and receiverID and content:
                await self.save_message(CHistoryID, senderID, receiverID, content)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'CHistoryID': CHistoryID,
                        'senderID': senderID,
                        'receiverID': receiverID,
                        'content': content
                    }
                )

    async def chat_message(self, event):
        print(f"Sending message: {event}")
        await self.send(text_data=json.dumps({
            'CHistoryID': event['CHistoryID'],
            'senderID': event['senderID'],
            'receiverID': event['receiverID'],
            'content': event['content']
        }))

    @database_sync_to_async
    def save_message(self, CHistoryID, senderID, receiverID, content):
        from .models import ChatRoom, AppUser, Chat  # 여기에 모델 임포트
        chat_room = ChatRoom.objects.get(HistoryID=CHistoryID)
        sender = AppUser.objects.get(iD=senderID)
        receiver = AppUser.objects.get(userID=receiverID)
        Chat.objects.create(
            CHistoryID=chat_room,
            senderID=sender,
            receiverID=receiver,
            content=content
        )

    @database_sync_to_async
    def load_initial_messages(self, chatRoomId):
        from .models import Chat  # 여기에 모델 임포트
        messages = Chat.objects.filter(CHistoryID=chatRoomId).order_by('timestamp')
        initial_messages = [{"CHistoryID": msg.CHistoryID.HistoryID, "senderID": msg.senderID.iD, "receiverID": msg.receiverID.iD, "content": msg.content} for msg in messages]
        return initial_messages

    async def send_initial_messages(self, initial_messages):
        await self.send(text_data=json.dumps({
            'type': 'initial_messages',
            'messages': initial_messages
        }))

    async def receive(self, text_data):
        print(f"Received message: {text_data}")
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'initial_load':
            chatRoomId = data.get('chatRoomId')
            if chatRoomId:
                initial_messages = await self.load_initial_messages(chatRoomId)
                await self.send_initial_messages(initial_messages)
        else:
            CHistoryID = data.get('CHistoryID')
            senderID = data.get('senderID')
            receiverID = data.get('receiverID')
            content = data.get('content')

            if CHistoryID and senderID and receiverID and content:
                await self.save_message(CHistoryID, senderID, receiverID, content)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'CHistoryID': CHistoryID,
                        'senderID': senderID,
                        'receiverID': receiverID,
                        'content': content
                    }
                )
