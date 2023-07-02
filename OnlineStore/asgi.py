"""
ASGI config for OnlineStore project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""
from django.core.asgi import get_asgi_application
default_http_settings = get_asgi_application()
import os
from ProductsBase import SocketHandlers
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineStore.settings')

application = ProtocolTypeRouter({

    "https": default_http_settings,

    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r"chat/", SocketHandlers.ConsumerChatHandler.as_asgi()),
                re_path(r"SupportStaff/(?P<Client_ID>\w+)/", SocketHandlers.AdminChatHandler.as_asgi()),
                re_path(r"ClientsMonitor/", SocketHandlers.Admin_Clients_Notification.as_asgi()),
            ])
        )
    ),
})
