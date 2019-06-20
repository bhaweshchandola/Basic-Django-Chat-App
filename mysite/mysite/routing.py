# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from channels.sessions import SessionMiddlewareStack

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': SessionMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.sessions import SessionMiddlewareStack

# from chat import consumers

# application = ProtocolTypeRouter({

#     "websocket": SessionMiddlewareStack(
#         URLRouter([
#             url(r"^front(end)/$", consumers.AsyncChatConsumer),
#         ])
#     ),

# })