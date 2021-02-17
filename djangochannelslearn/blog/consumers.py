# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
import requests
from asgiref.sync import async_to_sync
from blog.models import Blog


class BlogConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "blog"
        self.room_group_name = 'blogroom'
        self.user = self.scope["user"]
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.accept())

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)

        # Send message to room group
        self.parse_message(data)

    # Receive message from room group
    def parse_message(self, data):
        event_type = data['event_type']

        # Send message to WebSocket
        if event_type == 'load_message':
            self.load_message()
        else:
            self.send_message(data['message'])

    def load_message(self):
        response_obj = {"resp": []}
        for i in Blog.last_10_messages():
            response_obj["resp"].append(self.convert_to_json(i))
            print(self.convert_to_json(i))
        return json.dumps(response_obj)

    def convert_to_json(self, blog_object):
        blog_dict = {'author': blog_object.author.username, 'post': blog_object.post}
        return blog_dict

    def send_message(self, message):
        print("recived message {}",message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        print(self.user)
        blog = Blog(author=self.user, post=message)
        blog.save()

    def chat_message(self, event):
        message = event['message']
        print("gfchg")
        self.send(text_data=json.dumps({
            'message': message
        }))