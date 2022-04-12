from django.urls import path
from send.views import *

app_name = 'send'

urlpatterns = [
    path('send-egpx/', send_egpx, name='send-egpx'),
    path('send-eip/', send_eip, name='send-eip'),
    path('send-eop/', send_eop, name='send-eop'),
    path('send-ecp/', send_ecp, name='send-ecp'),
]