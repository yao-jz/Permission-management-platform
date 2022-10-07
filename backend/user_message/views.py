from typing import Dict, Any
from django.http.request import HttpRequest
from django.http.response import JsonResponse

from utils.decorators import POST_only, JSON_POST, login_needed, NeedFields, judge_from_to
from utils.const import RequestFieldConst, JsonResponseDictConst
from utils.views import generate_json_response_dict

from .models import UserMessage

# Create your views here.


@POST_only
@JSON_POST
@login_needed
@NeedFields([RequestFieldConst.FROM, RequestFieldConst.TO], [int, int])
@judge_from_to
def recv_message_list(request: HttpRequest, param_dict: Dict[str, Any], **wargs) -> JsonResponse:
    '''
    获得用户接受的所有信息的列表（POST），需要登录

    url: /message/recv_list

    { 
        from: int,
        to: int,
    }
        =>
    {
        status: string,
        msg: string,
        list: [
            {
                created_time: string,
                message: string,
                title: string,
                from: string,
                to: string
            }
        ]
    }
    '''

    return_messages = UserMessage.objects.filter(to_user=request.user).order_by('-created_time')
    from_int = param_dict[RequestFieldConst.FROM]
    to_int = param_dict[RequestFieldConst.TO]

    if from_int > 0 and return_messages.count() <= from_int:
        return JsonResponse(generate_json_response_dict(False, 
            f'from is too big ({JsonResponseDictConst.ErrorMessage.FROM_INT_TOO_BIG})'))

    return_list = [message.to_dict() for message in return_messages[from_int: to_int]]
    return JsonResponse(generate_json_response_dict(
        list = return_list
    ))

@POST_only
@JSON_POST
@login_needed
@NeedFields([RequestFieldConst.FROM, RequestFieldConst.TO], [int, int])
@judge_from_to
def send_message_list(request: HttpRequest, param_dict: Dict[str, Any], **wargs) -> JsonResponse:
    '''
    获得用户发出的所有信息的列表（POST），需要登录

    url: /message/sended_list

    { 
        from: int,
        to: int,
    }
        =>
    {
        status: string,
        msg: string,
        list: [
            {
                created_time: string,
                message: string,
                title: string,
                from: string,
                to: string
            }
        ]
    }
    '''

    return_messages = UserMessage.objects.filter(from_user=request.user).order_by('-created_time')
    from_int = param_dict[RequestFieldConst.FROM]
    to_int = param_dict[RequestFieldConst.TO]

    if from_int > 0 and return_messages.count() <= from_int:
        return JsonResponse(generate_json_response_dict(False, 
            f'from is too big ({JsonResponseDictConst.ErrorMessage.FROM_INT_TOO_BIG})'))

    return_list = [message.to_dict() for message in return_messages[from_int: to_int]]
    return JsonResponse(generate_json_response_dict(
        list = return_list
    ))
