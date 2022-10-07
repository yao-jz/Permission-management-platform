from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_info, name='get_info'),
    path('reset_all', views.reset_all_info, name='reset_all'),
    path('avatar', views.change_avatar, name='avatar'),
    path('edit', views.edit, name='edit'),
]
