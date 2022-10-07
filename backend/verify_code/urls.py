from django.urls import path
from . import views

urlpatterns = [
    path('url', views.verify_url, name='url'),
    path('code', views.verify_code, name='code'),
]
