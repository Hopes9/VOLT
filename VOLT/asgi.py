# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from channels.sessions import SessionMiddlewareStack
# from notifications.middlewares import WebSocketJWTAuthMiddleware
# from VOLT.routing import websocket_urlpatterns

import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VOLT.settings')
django.setup()
application = get_asgi_application()
# application = ProtocolTypeRouter({
#     "websocket":
#         AllowedHostsOriginValidator(
#             SessionMiddlewareStack(
#                 WebSocketJWTAuthMiddleware(
#                     URLRouter(
#                         websocket_urlpatterns
#                     )
#                 )
#             )
#         ),
# })
