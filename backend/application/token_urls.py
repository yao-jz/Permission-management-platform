from django.urls import path
from . import token_views

urlpatterns = [
    path('delete', token_views.delete_token, name='delete'),
    path('change', token_views.change_token, name='change'),
]
