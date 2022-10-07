import datetime
import threading
import time

from typing import Any, Dict, Union
from pytz import UTC
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http.request import HttpRequest
from django.http.response import JsonResponse, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import get_user_model

from utils.const import BackendConst, RequestFieldConst
from utils.decorators import GET_only, JSON_POST, NeedFields, POST_only
from utils.views import generate_json_response_dict

from .models import EmailVerifyCode

# Create your views here.

User = get_user_model()


def email_html_content() -> str:
    '''
    将html模板读入内存中，避免每次发邮件都要进行文件操作
    '''

    return_str = ''
    with open(BackendConst.DEFAULT_VERIFY_EMAIL_HTML, 'r', encoding='utf-8') as email_html:
        return_str = email_html.read()
    return return_str

EMAIL_HTML_CONTENT = email_html_content()
EMAIL_TEXT_CONTENT = '''
    企业通用权限平台邮箱验证
    尊敬的用户：
        您好，您正在用此邮箱绑定您在企业通用权限平台的帐号，请输入下方验证码完成邮箱绑定：
        {{verify_code}}
        如果您未使用过企业通用权限平台或未进行过绑定邮箱的操作，请忽略本邮件。
    '''

@GET_only
@NeedFields([RequestFieldConst.URL_PARAM, RequestFieldConst.EMAIL], [str, str])
def verify_url(request: HttpRequest, param_dict: Dict[str, Any]) -> Union[JsonResponse, HttpResponse]:
    '''
    用户点击邮件的链接后自动进入这个接口

    验证通过后关联帐号和邮箱，然后展示页面

    url: /veirfy/url

    {
        param: string,
        email: string,
    }
        =>
    html | {
        msg: string,
        status: string,
    }
    '''

    email = param_dict[RequestFieldConst.EMAIL]
    url_param = param_dict[RequestFieldConst.URL_PARAM]

    verify_objects = EmailVerifyCode.objects.filter(email=email, url_param=url_param)
    if not verify_objects.exists():
        return render(request, 'email_verify_error.html')

    verify_object = verify_objects.first()
    if verify_object.created_time + EmailVerifyCode.DEFAULT_TIME_OUT <= datetime.datetime.now(UTC):
        verify_object.delete()
        return render(request, 'email_verify_error.html')

    verify_object.user.email = verify_object.email
    verify_object.user.save()
    verify_object.delete()

    return render(request, 'email_verify_success.html', {
        'email': email,
    })

@POST_only
@JSON_POST
@NeedFields([RequestFieldConst.CODE, RequestFieldConst.EMAIL], [str, str])
def verify_code(request: HttpRequest, param_dict: Dict[str, Any]) -> JsonResponse:
    '''
    使用验证码验证邮箱（POST）

    验证通过后关联帐号和邮箱

    url: /veirfy/code

    {
        code: string,
        email: string,
    }
        =>
    {
        msg: string,
        status: string,
    }
    '''

    code = param_dict[RequestFieldConst.CODE]
    email = param_dict[RequestFieldConst.EMAIL]

    verify_objects = EmailVerifyCode.objects.filter(email=email, code=code)
    if not verify_objects.exists():
        return JsonResponse(generate_json_response_dict(False))

    verify_object = verify_objects.first()
    if verify_object.created_time + EmailVerifyCode.DEFAULT_TIME_OUT <= datetime.datetime.now(UTC):
        verify_object.delete()
        return JsonResponse(generate_json_response_dict(False))

    verify_object.user.email = verify_object.email
    verify_object.user.save()
    verify_object.delete()

    return JsonResponse(generate_json_response_dict())

def send_verify_email(email: str, user: User) -> bool:
    '''
    向指定的email发送验证邮件，并自动将验证信息存入数据库

    返回一个布尔值，指示是否发送成功
    '''

    verify_object = EmailVerifyCode.create_verify_code(email, user)
    if verify_object is None:
        return False

    html_content = EMAIL_HTML_CONTENT.replace(
        BackendConst.VerifyEmailPlaceHolder.VERIFY_URL, 
        BackendConst.BACKEND_HOST + reverse('verify:url') + f'?{RequestFieldConst.URL_PARAM}={verify_object.url_param}'
            + f'&{RequestFieldConst.EMAIL}={email}'
    ).replace(
        BackendConst.VerifyEmailPlaceHolder.VERIFY_CODE, 
        str(verify_object.code)
    )

    text_content = EMAIL_TEXT_CONTENT.replace(
        BackendConst.VerifyEmailPlaceHolder.VERIFY_CODE,
        str(verify_object.code)
    )

    verify_email = EmailMultiAlternatives('通用权限平台邮箱验证', text_content, settings.DEFAULT_FROM_EMAIL, [email])
    verify_email.attach_alternative(html_content, 'text/html')

    return bool(verify_email.send())
    

class EmailVerifyCodeManager:
    '''
    用于定期删除过期EmailVerifyCode的管理类，采用单例模式
    '''

    _INSTANCE_LOCK = threading.Lock()
    TIME_DELTA = datetime.timedelta(hours=1)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_INSTANCE"):
            with cls._INSTANCE_LOCK:
                if not hasattr(EmailVerifyCodeManager, "_INSTANCE"):
                    cls._INSTANCE = object.__new__(cls)
        return cls._INSTANCE
        
    def clear_time_out_codes(self) -> None:
        while True:
            time.sleep(self.TIME_DELTA.total_seconds())
            
            time_out_tokens = EmailVerifyCode.objects.filter(created_time__lte=datetime.datetime.now(UTC) - self.TIME_DELTA)
            time_out_tokens.delete()

    def __init__(self):
        clear_thread = threading.Thread(target=self.clear_time_out_codes)
        clear_thread.setDaemon(True)
        clear_thread.start()

EMAIL_VERIFY_CODE_MANAGER = EmailVerifyCodeManager()
