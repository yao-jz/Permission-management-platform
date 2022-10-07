import json
import sys

from typing import Iterable, Union, Dict, Any
from django.http.response import JsonResponse
from django.http.request import HttpRequest, QueryDict
from django.contrib.auth import authenticate
from django.contrib import auth
from django.conf import settings

from .views import generate_json_response_dict, get_request_field
from .const import JsonResponseDictConst, RequestFieldConst


def deprecated_function(func):
    '''
    标注该函数被弃用，如果使用则整个程序直接退出
    '''

    def deprecated(*args, **wargs):
        print('deprecated function!')
        sys.exit(-1)
    return deprecated

def debug_view(view_function):
    '''
    标注该view函数用于Debug环境

    如果不是Debug环境直接返回说明错误的JsonResponse
    '''

    def for_debug(*args, **wargs) -> JsonResponse:
        if not settings.DEBUG:
            return JsonResponse(generate_json_response_dict(False, 'this api is for debug'))
        return view_function(*args, **wargs)

    return for_debug

def deprecated_view(view_function):
    '''
    标注该view函数已经被抛弃了，改为返回一个提示api已抛弃的JsonResponse
    '''

    def return_deprecate_json_responst(*_, **__):
        return JsonResponse(generate_json_response_dict(False, 'deprecated_view'))

    return return_deprecate_json_responst

def login_needed(view_function):
    '''
    标注该view函数需要用户已登录

    如果鉴权失败，改为返回一个提示鉴权失败的JsonResponse

    支持通过username和password来鉴权
    '''

    def check_login(request: HttpRequest, *args, **wargs) -> JsonResponse:
        if request.user.is_authenticated:
            return view_function(request, *args, **wargs)
        
        username = get_request_field(request, RequestFieldConst.USERNAME)
        password = get_request_field(request, RequestFieldConst.PASSWORD)
        if not username or not password:
            return JsonResponse(generate_json_response_dict(False, 
                msg=f'empty or no username or password ({JsonResponseDictConst.ErrorMessage.EMPTY_OR_NO_LOGIN_FIELDS})'
            ))

        username = str(username)
        password = str(password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return view_function(request, *args, **wargs)

        return JsonResponse(generate_json_response_dict(False, 
            msg=f'need login ({JsonResponseDictConst.ErrorMessage.LOGIN_FAIL})'
        ))

    return check_login

def judge_from_to(view_function):
    '''
    封装view_function中对from和to值的判断，首先会将负数拉为0，然后会判断是否能形成一个区间

    需要前置NeedFields修饰器，包含FROM和TO为int类型的判断

    仍然使用param_dict参数传参给view_function
    '''

    def from_to(*args, param_dict: Dict[str, Any], **wargs) -> JsonResponse:
        from_int = param_dict[RequestFieldConst.FROM]
        to_int = param_dict[RequestFieldConst.TO]
        from_int = max(0, from_int)
        to_int = max(0, to_int)

        if from_int >= to_int:
            return JsonResponse(generate_json_response_dict(False, '[from, to) didn\'t make sense'))

        param_dict[RequestFieldConst.FROM] = from_int
        param_dict[RequestFieldConst.TO] = to_int
        return view_function(*args, **wargs, param_dict=param_dict)

    return from_to

def method_only(view_function, method: str):
    '''
    标注该view函数只接受某种方式的请求

    否则返回提示仅接受该种请求的JsonResponse

    不要直接用作修饰器，请使用POST_only或GET_only
    '''

    def check_method(request: HttpRequest, *args, **wargs) -> JsonResponse:
        if request.method != method:
            return JsonResponse(generate_json_response_dict(False, 
                msg=f'only accept {method} request ({JsonResponseDictConst.ErrorMessage.METHOD_ONLY})'
            ))
        return view_function(request, *args, **wargs)

    return check_method

def POST_only(view_function):
    '''
    标注该view函数只接受POST请求

    否则返回提示仅接受POST请求的JsonResponse
    '''

    return method_only(view_function, 'POST')
    
def GET_only(view_function):
    '''
    标注该view函数只接受GET请求

    否则返回提示仅接受GET请求的JsonResponse
    '''

    return method_only(view_function, 'GET')

def JSON_POST(view_function):
    '''
    django不支持直接对json形式的POST请求解析，所以如果接受json形式POST，需要用这个装饰器封装

    如果请求头说明了是json类型且请求使用的是POST方法，则进行json解析；否则使用django的默认解析方法

    每次都会对整个body串进行解析，要适当安排装饰器的顺序
    '''

    def json_post(request: HttpRequest, *args, **wargs) -> JsonResponse:
        if 'application/json' in request.META.get('CONTENT_TYPE', '') and request.method == 'POST':
            try:
                data = json.loads(request.body)
            except:
                return JsonResponse(generate_json_response_dict(False, 'json parse error'))

            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            request.POST = query_dict

        return view_function(request, *args, **wargs)

    return json_post

class NeedFields:
    '''
    应当仅作为装饰器使用，用法：

    @NeedFields([field_str_1, field_str_2, ...], [type_1, type_2, ...] ?)

    def view_function(request):

        ...

    检查接收到的所有域在request里面是否有，如果没有则返回相应错误

    如果第二个有参数，则应该是类型列表（如果有的域不用检查，用None或其它什么非类型量填充；不支持typing库的类型），检查对应位置的field_str指示的request参数值是否是对应类型的

    如果没有域或者该域的类型检查不成功，会返回相应的错误提示信息

    被装饰的函数请提供一个param_dict参数来接受按顺序进行类型转换后参数列表（如果没有指定想要的类型就存直接从request得到的值）；如果不需要也请加上**wargs参数来避免函数传参错误
    '''

    def __init__(self, field_strings: Iterable[str], needed_types: Union[Iterable[type], None] = None):
        '''
        应当仅作为装饰器使用，用法：

        @NeedFields([field_str_1, field_str_2, ...], [type_1, type_2, ...] ?)

        def view_function(request):

            ...

        检查接收到的所有域在request里面是否有，如果没有则返回相应错误

        如果第二个有参数，则应该是类型列表（如果有的域不用检查，用None或其它什么非类型量填充；不支持typing库的类型），检查对应位置的field_str指示的request参数值是否是对应类型的

        如果没有域或者该域的类型检查不成功，会返回相应的错误提示信息

        被装饰的函数请提供一个param_dict参数来接受按顺序进行类型转换后参数列表（如果没有指定想要的类型就存直接从request得到的值）；如果不需要也请加上**wargs参数来避免函数传参错误
        '''

        self.field_strings = field_strings
        self.needed_types = needed_types

    def __call__(self, view_function):
        def need_fields(request: HttpRequest, *arg, **warg) -> JsonResponse:
            error_msg = ''
            needed_type_len = 0 if self.needed_types is None else len(self.needed_types)

            param_dict = {}

            for i in range(len(self.field_strings)):
                field_string = self.field_strings[i]
                field_value = get_request_field(request, field_string)

                if field_value is None:
                    error_msg += f'request has no field "{field_string}";'
                    continue
                
                if i < needed_type_len:
                    needed_type = self.needed_types[i]
                    if not isinstance(needed_type, type):
                        param_dict[field_string] = field_value
                        continue

                    try:
                        param_dict[field_string] = needed_type(field_value)
                    except:
                        error_msg += f'value of request field "{field_string}": "{field_value}" dosen\'t match the required type "{needed_type}";'
                        continue
                else:
                    param_dict[field_string] = field_value

            if error_msg != '':
                return JsonResponse(generate_json_response_dict(False, error_msg))
            else:
                return view_function(request, *arg, **warg, param_dict=param_dict)

        return need_fields
