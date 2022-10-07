from typing import Dict, Any
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model

from verify_code.views import send_verify_email
from utils.decorators import debug_view, POST_only, JSON_POST, login_needed, NeedFields
from utils.views import generate_json_response_dict
from utils.const import JsonResponseDictConst, RequestFieldConst

from .models import UserInfo

# Create your views here.

User = get_user_model()


def get_user_info(user: User) -> UserInfo:
    '''
    获得user绑定的info

    如果没有绑定，则自动新建一个
    '''

    if not UserInfo.objects.filter(user=user).exists():
        UserInfo.create_for_user(user)
    return user.info

def reset_info(user: User) -> UserInfo:
    '''
    将用户的UserInfo重设回默认
    '''

    info = UserInfo.objects.filter(user=user)

    if info.exists():
        info.delete()

    return get_user_info(user)

def create_user(**wargs) -> User:
    '''
    将原本传给User.objects.create_user的参数传过来

    自动新建匹配的UserInfo
    '''

    user = User.objects.create_user(**wargs)
    UserInfo.create_for_user(user)

    return user

@debug_view
def reset_all_info(request: HttpRequest) -> JsonResponse:
    for user in User.objects.all():
        reset_info(user)

    return JsonResponse(generate_json_response_dict())

@POST_only
@JSON_POST
@login_needed
def get_info(request: HttpRequest) -> JsonResponse:
    '''
    获得用户的信息，需要已登录

    url: /user_info/

    { }
        =>
    {
        status: string,
        msg: string,
        avatar: string,
    }
    '''

    info = get_user_info(request.user)
    return_dict = generate_json_response_dict()
    return_dict.update(info.to_dict())
    return_dict.update({
        JsonResponseDictConst.EMAIL: request.user.email,
    })
    
    return JsonResponse(return_dict)

@POST_only
@JSON_POST
@login_needed
def change_avatar(request: HttpRequest) -> JsonResponse:
    '''
    更改用户头像（POST）

    url: /user_info/avatar

    {
        file: file,
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    info = get_user_info(request.user).change_avatar(request.FILES.get('file', None))

    if info is None:
        return JsonResponse(generate_json_response_dict(False, 'save image failed'))
    return JsonResponse(generate_json_response_dict())

@POST_only
@JSON_POST
@login_needed
@NeedFields([RequestFieldConst.DETAIL], [dict])
def edit(request: HttpRequest, param_dict: Dict[str, Any]) -> JsonResponse:
    '''
    修改用户信息（POST），需要已登录

    url: /user_info/edit

    {
        detail: {
            username: string, ?
            password: string, ?
            email: string, ?
        }
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    detail = param_dict[RequestFieldConst.DETAIL]
    username = detail.get(RequestFieldConst.USERNAME, None)
    password = detail.get(RequestFieldConst.PASSWORD, None)
    email = detail.get(RequestFieldConst.EMAIL, None)

    warning_msg = ''

    if username is None:
        warning_msg += 'no username provided;'
    else:
        username = str(username)
        if username == '':
            warning_msg += 'username empty;'
        elif User.objects.filter(username=username).exists():
            warning_msg += 'username conflicts;'
        else:
            request.user.username = username
            request.user.save()

    if password is None:
        warning_msg += 'no password provided or empty password;'
    else:
        password = str(password)
        if password == '':
            warning_msg += 'password empty;'
        else:
            request.user.set_password(password)
            request.user.save()

    if email is None:
        warning_msg += 'no email provided or empty email;'
    else:
        email = str(email)
        send_result = send_verify_email(email, request.user)
        if not send_result:
            warning_msg += 'email send failed;'

    return JsonResponse(generate_json_response_dict(
        msg=warning_msg
    ))
