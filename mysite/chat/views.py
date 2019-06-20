# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
from asgiref.sync import async_to_sync
# from asgi import channel_layer

def index(request):
    channel_layer = get_channel_layer()
    request.session["seed"] = "chat"
    print(request.session["seed"])
    async_to_sync(channel_layer.group_send)(request.session["seed"], {
                'type': 'chat_message',
                'message': "message"
            })

    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })