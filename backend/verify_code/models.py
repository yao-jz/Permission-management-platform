import datetime

from typing import Union
from pytz import UTC
from django.db import models
from django.contrib.auth import get_user_model

from utils.views import generate_random_str

# Create your models here.

User = get_user_model()


class VerifyCode(models.Model):
    '''
    验证码基类

    抽象类，这个类不会存入数据库

    - created_time: 创建时间
    - code: 验证码内容
    - url_param: 验证链接的相关参数
    '''

    class Meta:
        abstract = True

    DEFAULT_TIME_OUT = datetime.timedelta(minutes=5)
    DEFAULT_CODE_LENGTH = 9
    DEFAULT_CODE_CHARS = '0123456789'
    DEFAULT_URL_PARAM_LENGTH = 30
    DEFAULT_URL_PARAM_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-0123456789()*^|'

    created_time = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=DEFAULT_CODE_LENGTH, blank=True, default='')
    url_param = models.CharField(max_length=DEFAULT_URL_PARAM_LENGTH, blank=True, default='')


class EmailVerifyCode(VerifyCode):
    '''
    邮箱验证码
    - email: 关联的邮箱
    - user: 邮箱希望关联的用户
    - created_time: 创建时间
    - code: 验证码内容
    - url_param: 验证链接的相关参数
    '''

    email = models.EmailField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='verify_emails')

    @classmethod
    def create_verify_code(cls, email: str, user: User) -> Union['EmailVerifyCode', None]:
        '''
        生成一个新的验证码对象，如果传入的邮箱不合法则返回None
        '''

        try:
            new_verify = cls.objects.create(
                email = email,
                user = user
            )
        except:
            return None

        code = generate_random_str(cls.DEFAULT_CODE_LENGTH, cls.DEFAULT_CODE_CHARS)
        while True:
            possible_codes = cls.objects.filter(code=code)
            if not possible_codes.exists():
                break
            possible_code = possible_codes.first()
            if possible_code.created_time + cls.DEFAULT_TIME_OUT <= datetime.datetime.now(UTC):
                possible_code.delete()
                break
            code = generate_random_str(cls.DEFAULT_CODE_LENGTH, cls.DEFAULT_CODE_CHARS)
        new_verify.code = code
        new_verify.save()

        url_param = generate_random_str(cls.DEFAULT_URL_PARAM_LENGTH, cls.DEFAULT_URL_PARAM_CHARS)
        while True:
            possible_codes = cls.objects.filter(url_param=url_param)
            if not possible_codes.exists():
                break
            possible_code = possible_codes.first()
            if possible_code.created_time + cls.DEFAULT_TIME_OUT <= datetime.datetime.now(UTC):
                possible_code.delete()
                break
            url_param = generate_random_str(cls.DEFAULT_URL_PARAM_LENGTH, cls.DEFAULT_URL_PARAM_CHARS)
        new_verify.url_param = url_param
        new_verify.save()

        return new_verify
