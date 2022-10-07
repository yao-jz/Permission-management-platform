from django.urls import path
from . import root_views

urlpatterns = [
    path('login', root_views.login, name='login'),
    path('logout', root_views.logout, name='logout'),
    path('register', root_views.register, name='register'),
    path('delete', root_views.delete_user, name='delete'),
]
