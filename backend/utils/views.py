import sys
import random

from typing import Any, Dict, Union
from django.http.request import HttpRequest

from .models import SetModelStatus
from .const import JsonResponseDictConst, RequestFieldConst

def general_set_model_check(cls: type, key: Union[str, None] = None, name: Union[str, None] = None, 
    description: Union[None, str] = None) -> SetModelStatus:
    '''
    三个ApplicationXXX类新建对象时应该执行的例行方法
    
    检查是否符合一定条件，包括：
    - EMPTY_NAME
    - EMPTY_KEY
    - KEY_TOO_LONG
    - NAME_TOO_LONG
    - DESCRIPTION_TOO_LONG
    - INVALID_KEY_CHAR
    - KEY_NOT_STR
    - NAME_NOT_STR
    - DESCRIPTION_NOT_STR
    '''

    if key is not None:
        if not isinstance(key, str):
            return SetModelStatus.KEY_NOT_STR
        elif key == '':
            return SetModelStatus.EMPTY_KEY
        elif len(key) > cls.MAX_KEY_LENGTH:
            return SetModelStatus.KEY_TOO_LONG
        for char in key:
            if char not in cls.KEY_CHARS:
                return SetModelStatus.INVALID_KEY_CHAR

    if name is not None:
        if not isinstance(name, str):
            return SetModelStatus.NAME_NOT_STR
        elif name == '':
            return SetModelStatus.EMPTY_NAME
        elif len(name) > cls.MAX_NAME_LENGTH:
            return SetModelStatus.NAME_TOO_LONG

    if description is not None:
        if len(description) > cls.MAX_DESCRIPTION_LENGTH:
            return SetModelStatus.DESCRIPTION_TOO_LONG

    return SetModelStatus.SUCCEED


def general_set_model_check_for_application(cls: type, key: Union[str, None] = None, name: Union[str, None] = None,
                            description: Union[None, str] = None) -> SetModelStatus:
    '''
    Application类新建对象时应该执行的例行方法

    检查是否符合一定条件，包括：
    - EMPTY_NAME
    - EMPTY_KEY
    - KEY_TOO_LONG
    - NAME_TOO_LONG
    - DESCRIPTION_TOO_LONG
    - KEY_NOT_STR
    - NAME_NOT_STR
    - DESCRIPTION_NOT_STR
    '''

    if key is not None:
        if not isinstance(key, str):
            return SetModelStatus.KEY_NOT_STR
        elif key == '':
            return SetModelStatus.EMPTY_KEY
        elif len(key) > cls.MAX_KEY_LENGTH:
            return SetModelStatus.KEY_TOO_LONG

    if name is not None:
        if not isinstance(name, str):
            return SetModelStatus.NAME_NOT_STR
        elif name == '':
            return SetModelStatus.EMPTY_NAME
        elif len(name) > cls.MAX_NAME_LENGTH:
            return SetModelStatus.NAME_TOO_LONG

    if description is not None:
        if len(description) > cls.MAX_DESCRIPTION_LENGTH:
            return SetModelStatus.DESCRIPTION_TOO_LONG

    return SetModelStatus.SUCCEED

def generate_json_response_dict(succeed: bool = True, msg: str = '', **dict_args) -> Dict[str, Any]:
    '''
    自动填充status和msg信息，生成返回的dict
    '''

    dict_args[JsonResponseDictConst.STATUS] = JsonResponseDictConst.SUCCEED if succeed else JsonResponseDictConst.FAIL
    dict_args[JsonResponseDictConst.MSG] = msg

    return dict_args

def get_request_field(request: HttpRequest, field: str) -> Any:
    '''
    获得请求的某个GET或者POST的字段，如果不存在则返回None

    如果是传入RequestFieldConst.TYPE或者RequestFieldConst.WANTED_TYPE，则合法时会自动返回为RequestFieldConst.OperateType类型
    '''

    if field == RequestFieldConst.TYPE:
        return RequestFieldConst.get_request_type_field(request)
    elif field == RequestFieldConst.WANTED_TYPE:
        return RequestFieldConst.get_request_type_field(request, RequestFieldConst.WANTED_TYPE)

    if request.method == 'GET':
        return request.GET.get(field, default=None)
    elif request.method == 'POST':
        return request.POST.get(field, default=None)
    else:
        return None

def generate_random_str(length: int, usable_chars: str = '0123456789') -> str:
    '''
    随机生成字符串
    '''

    random.seed()
    usable_chars_len = len(usable_chars)

    return_str = ''
    for _ in range(length):
        return_str += usable_chars[random.randint(0, usable_chars_len - 1)]

    return return_str

def transform_html(raw_content: str) -> str:
    '''
    将初始的字符串中的一些特殊字符替换为对应的html转义符
    '''

    return raw_content.replace('&', '&amp;'
    ).replace('<', '&lt;'
    ).replace('>', '&gt;'
    ).replace('\n', '<br>'
    ).replace('\t', '    '
    ).replace(' ', '&ensp'
    ).replace('　', '&emsp'
    )
