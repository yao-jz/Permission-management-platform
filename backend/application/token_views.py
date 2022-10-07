import datetime

from typing import Dict, Any, Union
from pytz import UTC
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model

from user_app_relation.models import UserApplicationRelation
from application_token.models import ApplicationToken
from utils.decorators import POST_only, JSON_POST, login_needed, NeedFields
from utils.const import RequestFieldConst, JsonResponseDictConst
from utils.views import generate_json_response_dict

from .models import Application

User = get_user_model()


@POST_only
@JSON_POST
@login_needed
@NeedFields([RequestFieldConst.LIST], [list])
def delete_token(request: HttpRequest, param_dict: Dict[str, Any]) -> JsonResponse:
    '''
    删除app_token（POST），需要登录

    url: /token/delete

    {
        list: [
            {
                app_key: string,
                app_token: string,
            }
        ],
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    warning_msg = ''

    for token_info in param_dict[RequestFieldConst.LIST]:
        if not isinstance(token_info, dict):
            warning_msg += (f'token_info "{token_info}" not a dict ' +
                f'({JsonResponseDictConst.ErrorMessage.PARSE_MESS});')
            continue

        token_string = token_info.get(RequestFieldConst.APP_TOKEN, None)
        app_key = token_info.get(RequestFieldConst.APP_KEY, None)

        if token_string is None or app_key is None:
            warning_msg += (f'token_info "{token_info}" dose\'nt have app_key or app_token ' +
                f'({JsonResponseDictConst.ErrorMessage.NO_REQUIRED_FIELD});')
            continue

        token_string = str(token_string)
        app_key = str(app_key)

        application, token_access = Application.get_application_by_token_string(token_string, app_key)
        if application is None:
            warning_msg += (f'token_string "{token_string}" not attached ' +
                f'({JsonResponseDictConst.ErrorMessage.TOKEN_ATTACH_NO_APPLICATION});')
            continue

        user_access = application.get_user_access(request.user)

        if not user_access.check_access(UserApplicationRelation.UserAccessStatus.ADMIN):
            warning_msg += (f'user has no access to application attached by token "{token_string}" ' +
                f'({JsonResponseDictConst.ErrorMessage.ACCESS_ERROR});')
            continue

        if user_access.value > token_access.value:
            warning_msg += (f'user access lower than token access of token "{token_string}" ' + 
                f'({JsonResponseDictConst.ErrorMessage.ACCESS_ERROR});')
            continue

        ApplicationToken.objects.filter(application=application, content=token_string).delete()

    return JsonResponse(generate_json_response_dict(
        msg=warning_msg
    ))

def change_token_time(token: ApplicationToken, alive_time: Union[Any, None] = None) -> str:
    '''
    尝试改变token_info指定的token和其时限，返回警告信息

    调用之前应该已经判断过用户是否能改变该token的时限

    不要用来接受url，应该仅用于change_token函数调用
    '''

    if alive_time is None:
        return ''

    alive_time = str(alive_time)
    if alive_time == RequestFieldConst.FOREVER:
        token.forever = True
        token.save()
        return ''

    try:
        alive_time = int(alive_time)
    except ValueError:
        return f'alive_time "{alive_time}" not an int ({JsonResponseDictConst.ErrorMessage.PARSE_MESS});'

    if alive_time < 0:
        return f'alive_time "{alive_time}" < 0 ({JsonResponseDictConst.ErrorMessage.PARSE_MESS});'

    token.dead_time = datetime.datetime.now(UTC) + datetime.timedelta(seconds=alive_time)
    token.forever = False
    token.save()
    return ''

def change_token_access(token: ApplicationToken, user: User, new_access: Union[Any, None] = None) -> str:
    '''
    尝试以user的身份改变token_info指定的token和其权限，返回警告信息

    不要用来接受url，应该仅用于change_token函数调用
    '''

    if new_access is None:
        return ''

    try:
        new_access = ApplicationToken.ApplicationAccessStatus(int(new_access))
    except ValueError:
        return f'new access "{new_access}" does\'nt make sense ({JsonResponseDictConst.ErrorMessage.PARSE_MESS});'
    
    application: Application = token.application
    if application.get_user_access(user).value > new_access.value:
        return f'user access lower than new access "{new_access}" ({JsonResponseDictConst.ErrorMessage.ACCESS_ERROR});'

    token.access = new_access.value
    token.save()
    return ''

@POST_only
@JSON_POST
@login_needed
@NeedFields([RequestFieldConst.LIST], [list])
def change_token(request: HttpRequest, param_dict: Dict[str, Any]) -> JsonResponse:
    '''
    修改app_token期限和权限（POST），需要登录

    alive_time可以用int类型的数据表示期限的秒数（需为正数），也可以写forever，表示设为永久

    url: /token/change

    {
        list: [
            {
                app_key: string,
                app_token: string,
                alive_time: int | string("forever"), ?
                token_access: int, ?
            }
        ]
    }
        =>
    {
        status: string,
        msg: string,
        list: [
            {
                content: string,
                created_time: string,
                dead_time: string,
                access: string,
            } | {}
        ]
    }
    '''

    warning_msg = ''
    return_list = []

    for token_info in param_dict[RequestFieldConst.LIST]:
        if not isinstance(token_info, dict):
            warning_msg += (f'token_info "{token_info}" failed to parse to dict ' +
                f'({JsonResponseDictConst.ErrorMessage.PARSE_MESS});')
            return_list += [{}]
            continue

        token_string = token_info.get(RequestFieldConst.APP_TOKEN, None)
        app_key = token_info.get(RequestFieldConst.APP_KEY, None)

        if token_string is None or app_key is None:
            warning_msg += (f'token_info "{token_info}" has no app_token or app_key '
                f'({JsonResponseDictConst.ErrorMessage.NO_REQUIRED_FIELD});')
            return_list += [{}]
            continue

        token_string = str(token_string)
        app_key = str(app_key)

        application, token_access = Application.get_application_by_token_string(token_string, app_key)
        if application is None:
            warning_msg += (f'token "{token_string}" attaches no application ' +
                f'({JsonResponseDictConst.ErrorMessage.TOKEN_ATTACH_NO_APPLICATION});')
            return_list += [{}]
            continue

        user_access = application.get_user_access(request.user)

        if not user_access.check_access(UserApplicationRelation.UserAccessStatus.ADMIN):
            warning_msg += (f'user access not enough to application attached by "{token_string}" ' + 
                f'({JsonResponseDictConst.ErrorMessage.ACCESS_ERROR});')
            return_list += [{}]
            continue

        if user_access.value > token_access.value:
            warning_msg += (f'user access lower than token access "{token_string}" ' +
                f'({JsonResponseDictConst.ErrorMessage.ACCESS_ERROR});')
            return_list += [{}]
            continue

        application_token = ApplicationToken.objects.filter(application=application, content=token_string).first()
        initial_access = application_token.access

        change_time_msg = change_token_time(
            token=application_token, 
            alive_time=token_info.get(RequestFieldConst.ALIVE_TIME, None)
        )
        warning_msg += change_time_msg

        change_access_msg = change_token_access(
            token=application_token,
            user=request.user,
            new_access=token_info.get(RequestFieldConst.TOKEN_ACCESS, None)
        )
        warning_msg += change_access_msg

        return_list += [application.get_tokens(initial_access, exact_access=True).first().to_dict()]

    return JsonResponse(generate_json_response_dict(
        msg=warning_msg,
        list=return_list
    ))
