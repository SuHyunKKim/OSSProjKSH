"""
ASGI config for Kiri_prj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import Kiri_app.routing  # 라우팅 설정이 있는 모듈을 임포트하세요



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kiri_prj.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Kiri_app.routing.websocket_urlpatterns
        )
    ),
})