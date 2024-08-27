import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

# 메모리에 메시지 저장
message_history = []
MAX_MESSAGES = 100

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket 연결 시도")
        self.room_name = "chat"
        self.room_group_name = f"chat_{self.room_name}"

        # 그룹에 참여
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"WebSocket 연결 성공: {self.channel_name}")

        # 연결 시 이전 메시지 전송
        for message in message_history:
            await self.send(text_data=json.dumps(message))

    async def disconnect(self, close_code):
        logger.info(f"WebSocket 연결 종료 (코드: {close_code}): {self.channel_name}")
        # 그룹에서 나가기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        logger.info(f"메시지 수신: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = await self.get_username()

        # 메시지 저장
        message_data = {
            'message': message,
            'sender': sender
        }
        message_history.append(message_data)
        if len(message_history) > MAX_MESSAGES:
            message_history.pop(0)

        # 그룹에 메시지 보내기
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        logger.info(f"메시지 전송 준비: {sender}: {message}")

        # WebSocket으로 메시지 보내기
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
        logger.info(f"메시지 전송 완료: {sender}: {message}")

    @sync_to_async
    def get_username(self):
        return self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"