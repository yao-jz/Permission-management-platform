"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls import url
from django.views import static

urlpatterns = [
    path('', include(('application.root_urls', 'application'), namespace='root')),
    path('app/', include(('application.urls', 'application'), namespace='application')),
    path('token/', include(('application.token_urls', 'application'), namespace='token')),
    path('user_info/', include(('user_info.urls', 'user_info'), namespace='user_info')),
    path('verify/', include(('verify_code.urls', 'verify_code'), namespace='verify')),
    path('message/', include(('user_message.urls', 'user_message'), namespace='message')),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]
