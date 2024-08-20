
import os

from django.core.asgi import get_asgi_application
import django

# 채팅방
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

django.setup()

import myapp.routing
django_asgi_app = get_asgi_application()

# 채팅방
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            myapp.routing.websocket_urlpatterns
        )
    ),
})