from django.urls import path
from . import views

urlpatterns = [
    path('recv_list', views.recv_message_list, name='recv_list'),
    path('sended_list', views.send_message_list, name='sended_list'),
]
