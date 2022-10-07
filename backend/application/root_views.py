from typing import Dict
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model

import django.contrib.auth as django_auth

from user_info.views import create_user
from utils.decorators import POST_only, JSON_POST, login_needed, NeedFields
from utils.const import RequestFieldConst
from utils.views import generate_json_response_dict

User = get_user_model()


@POST_only
@JSON_POST
@NeedFields([RequestFieldConst.USERNAME, RequestFieldConst.PASSWORD], [str, str])
def login(request: HttpRequest, param_dict: Dict[str, str]) -> JsonResponse:
    '''
    用户登录（POST）
   
    url: /login

    {
        username: string,
        password: string,
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''
    
    username = param_dict[RequestFieldConst.USERNAME]
    password = param_dict[RequestFieldConst.PASSWORD]

    user = django_auth.authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse(generate_json_response_dict(False, 'username or password wrong'))

    django_auth.login(request, user)
    return JsonResponse(generate_json_response_dict())

@JSON_POST
@login_needed
def logout(request: HttpRequest) -> JsonResponse:
    '''
    用户登出（GET/POST），需要已经登录

    url: /logout

    { }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    django_auth.logout(request)
    return JsonResponse(generate_json_response_dict())

@POST_only
@JSON_POST
@NeedFields([RequestFieldConst.USERNAME, RequestFieldConst.PASSWORD], [str, str])
def register(request: HttpRequest, param_dict: Dict[str, str]) -> JsonResponse:
    '''
    用户注册（POST）

    url: /register

    {
        password: string,
        username: string,
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    username = param_dict[RequestFieldConst.USERNAME]
    password = param_dict[RequestFieldConst.PASSWORD]

    if password == '' or username == '':
        return JsonResponse(generate_json_response_dict(False, 'password or username empty'))
    if '{{' in username or '}}' in username:
        return JsonResponse(generate_json_response_dict(False, 'unusable username char (possibly {{ or }})'))

    if User.objects.filter(username=username).exists():
        return JsonResponse(generate_json_response_dict(False, 'username confilct'))

    user = create_user(username=username, password=password)
    django_auth.login(request, user)

    return JsonResponse(generate_json_response_dict())

@POST_only
@JSON_POST
@login_needed
def delete_user(request: HttpRequest) -> JsonResponse:
    '''
    永久删除用户（POST），需要已登录

    url: /delete

    { }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    request.user.delete()
    django_auth.logout(request)

    return JsonResponse(generate_json_response_dict())
    