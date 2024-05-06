import os

from channels.auth import AuthMiddlewareStack  # new import
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chat.routing
from chat.middleware import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JWTAuthMiddleware(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
