from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_application_list, name='list'),
    path('detail', views.get_detail, name='detail'),
    path('list', views.list_items, name='list_items'),
    path('attach', views.attach, name='attach'),
    path('detach', views.detach, name='detach'),
    path('check', views.check, name='check'),
    path('delete', views.delete, name='delete'),
    path('add', views.add, name='add'),
    path('show', views.show, name='show_related'),
    path('total', views.total, name='total'),
    path('description', views.get_description, name='description'),
    path('edit', views.edit, name='edit'),
    path('search', views.search, name='search'),
    path('share', views.share_application, name='share'),
    path('shared_list', views.get_shared_application_list, name='shared_list'),
    path('user_group', views.get_user_group, name='user_group'),
    path('send_message', views.send_message, name='send_message'),
    path('unshare', views.unshare_application, name='unshare'),
]
