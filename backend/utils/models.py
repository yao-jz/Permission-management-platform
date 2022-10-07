'''
本文件不应该涉及到数据库模型的定义，而是用于定义一些工具类
'''

from enum import Enum

# Create your models here.


class SetModelStatus(Enum):
    '''
    由于python的枚举类型不允许继承，故三个ApplicationXXX类的相关方法的返回状态均使用此类
    - SUCCEED
    - EMPTY_NAME
    - EMPTY_KEY
    - KEY_ALREADY_EXISTS
    - KEY_TOO_LONG
    - NAME_TOO_LONG
    - DESCRIPTION_TOO_LONG
    - INVALID_KEY_CHAR
    - KEY_NOT_STR
    - NAME_NOT_STR
    - DESCRIPTION_NOT_STR
    - NO_PARENT_OBJECT
    '''

    SUCCEED = 'succeed'
    UNEXPECTED_FAIL = 'an unexpected error occurred'
    EMPTY_NAME = 'empty name'
    EMPTY_KEY = 'empty key'
    KEY_ALREADY_EXISTS = 'key already exists'
    KEY_TOO_LONG = 'key too long'
    NAME_TOO_LONG = 'name too long'
    DESCRIPTION_TOO_LONG = 'description too long'
    INVALID_KEY_CHAR = 'invalid key char'
    KEY_NOT_STR = 'key is not a str'
    NAME_NOT_STR = 'name is not a str'
    DESCRIPTION_NOT_STR = 'description not a str'

    NO_PARENT_OBJECT = 'parent_key attaches no parent object'
