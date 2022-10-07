import os

from enum import Enum
from os.path import join
from typing import Union
from django.http.request import HttpRequest
from django.conf import settings


class JsonResponseDictConst:
    '''
    后端返回的常用键或值
    '''
    
    STATUS = 'status'
    SUCCEED = 'succeed'
    FAIL = 'fail'
    MSG = 'msg'
    TOTAL = 'total'
    LIST = 'list'  # 慎改，因为很多已经写死在代码里面了

    '''
    这些仅用于各个model的to_dict函数
    '''
    USER_NAME = 'name'
    USER_KEY = 'key'
    AUTH_NAME = 'name'
    AUTH_KEY = 'key'
    ROLE_NAME = 'name'
    ROLE_KEY = 'key'
    CREATED_TIME = 'created_time'
    DETACH_TIME = 'detach_time'
    CHILD_AUTHS = 'child_permissions'
    PARENT_AUTH = 'parent_permission'
    AVATAR = 'avatar'
    ACCESS = 'access'
    KEY = 'key'
    TITLE = 'title'
    FROM_USERNAME = 'from'
    TO_USERNAME = 'to'
    MESSAGE = 'message'

    EMAIL = 'email'

    class ErrorMessage:
        '''
        一些规定好的错误信息，一般嵌入返回信息的MSG中，方便编写测试
        '''

        FROM_INT_TOO_BIG = 'FROM_BIGGER_THAN_COUNT'
        USER_AND_APPLICATION_NOT_MATCH = 'APP_NOT_BELONG_TO_USER'
        METHOD_ONLY = 'METHOD_ONLY'
        EMPTY_OR_NO_LOGIN_FIELDS = 'EMPTY_OR_NO_LOGIN_FIELDS'
        LOGIN_FAIL = 'LOGIN_FAIL'
        TOKEN_ATTACH_NO_APPLICATION = 'TOKEN_ATTACH_NO_APPLICATION'
        PARSE_MESS = 'PARSE_FAIL'
        NO_REQUIRED_FIELD = 'NO_REQUIRED_FIELD'
        ACCESS_ERROR = 'ACCESS_ERROR'
        USER_NOT_FIND = 'USER_NOT_FIND'


class RequestFieldConst:
    '''
    放置了前端request域的一些通用字符串
    '''

    APP_TOKEN = 'app_token'
    APP_KEY = 'app_key'
    NEW_APP_KEY = 'new_app_key'
    TYPE = 'type'
    WANTED_TYPE = 'want_type'
    KEY = 'key'
    PARENT_KEY = 'parent_key'
    FROM = 'from'
    TO = 'to'
    KEYS = 'keys'
    LIST = 'list'
    NAME = 'name'
    DESCRIPTION = 'description'
    USERNAME = 'username'
    PASSWORD = 'password'
    DETAIL = 'detail'
    CONTENT = 'content'
    ALIVE_TIME = 'alive_time'
    TIME_OUT = 'time_out'
    
    # 这三个是用于attach和detach接口的，现在语义应该分别是USERS, AUTHS, ROLES
    USER_KEYS = 'user_keys'
    AUTH_KEYS = 'permission_keys'
    ROLE_KEYS = 'role_keys'

    EMAIL = 'email'
    URL_PARAM = 'param'
    CODE = 'code'

    TOKEN_ACCESS = 'token_access'
    FOREVER = 'forever'

    # App共享相关的
    USERNAME_SHARE = 'share_username'
    ACCESS = 'access'

    MESSAGE = 'message'
    TITLE = 'title'
    TO_USERNAME = 'to_username'

    class OperateType(Enum):
        '''
        针对前端请求的type域的结果

        获取该域请使用RequestFieldConst.get_request_type_field(request: HttpRequest)
        '''

        USER = 0
        ROLE = 1
        AUTH = 2

    @classmethod
    def get_request_type_field(cls, request: HttpRequest, specific_type_str: Union[str, None] = None) -> Union[None, 'RequestFieldConst.OperateType']:
        '''
        获取type域指定的OperateType的专用封装
        '''

        if specific_type_str is None:
            specific_type_str = cls.TYPE

        if request.method == "GET":
            type_str = request.GET.get(specific_type_str, default=None)
        elif request.method == 'POST':
            type_str = request.POST.get(specific_type_str, default=None)
        else:
            return None

        if type_str is None:
            return None

        try:
            return cls.OperateType(int(type_str))
        except:
            return None


class BackendConst:
    '''
    后端静态资源的路径常量
    '''

    DEMO_MEDIA_PATH = settings.BASE_DIR / 'demos'
    DEMO_AVATAR_PATH = os.path.join(DEMO_MEDIA_PATH, 'avatars')
    DEFAULT_USER_AVATAR = os.path.join(DEMO_AVATAR_PATH, 'demo.png')

    VERIFY_CODE_PATH = settings.BASE_DIR / 'verify_code'
    DEFAULT_VERIFY_EMAIL_HTML = os.path.join(VERIFY_CODE_PATH, 'email.html')

    USER_MESSAGE_PATH = settings.BASE_DIR / 'user_message'
    DEFAULT_MESSAGE_EMAIL_PATH = os.path.join(USER_MESSAGE_PATH, 'email.html')

    BACKEND_HOST = 'http://49.232.101.156:8000'

    PARAM_KEY = 'key'
    PARAM_NAME = 'name'
    PARAM_DESCRIPTION = 'description'

    class VerifyEmailPlaceHolder:
        VERIFY_CODE = '{{verify_code}}'
        VERIFY_URL = '{{verify_url}}'

    class MessageEmailPlaceHolder:
        FROM_AVATAR = '{{from_avatar}}'
        FROM_USERNAME = '{{from_username}}'
        APPLICATION_NAME = '{{application_name}}'
        MESSAGE = '{{message}}'
        TITLE = '{{title}}'


class TestConst:
    '''
    测试中会重复使用的常量
    '''

    JSON_CONTENT = "application/json"
    TEST_USER_AVATAR = os.path.join(BackendConst.DEMO_AVATAR_PATH, 'test.png')

    class RequestMethod(Enum):
        POST = 'POST'
        GET = 'GET'
