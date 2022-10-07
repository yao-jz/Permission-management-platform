from typing import Dict, Tuple, Union, Any
from enum import Enum
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.contrib.auth import get_user_model

from user_info.views import get_user_info
from utils.views import transform_html
from utils.const import BackendConst, JsonResponseDictConst

# Create your models here.

User = get_user_model()


def get_email_html() -> str:
    return_str = ''
    with open(BackendConst.DEFAULT_MESSAGE_EMAIL_PATH, 'r') as email:
        return_str = email.read()
    return return_str

EMAIL_HTML_CONTENT = get_email_html()
EMAIL_TEXT_CONTENT = '''
    企业通用平台用户提醒
        您的邮箱似乎不支持html内容展示 :(
        与您共同管理App "{{application_name}}" 的用户 "{{from_username}}" 向您发送了以下信息：
    ----------
    标题：{{title}}
    正文：
        {{message}}
    ----------
    '''

@shared_task
def send_message(user_message: 'UserMessage') -> None:
    '''
    使用celery异步来发送信息
    '''

    user_message.send_mail()


class UserMessage(models.Model):
    '''
    用户之间的交流信息
    - from_user: 发送信息的用户
    - to_user: 接受者
    - message: 信息内容
    - created_time: 创建时间
    '''

    MAX_MESSAGE_LENGTH = 300
    MAX_TITLE_LENGTH = 20

    from_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sended_messages')
    to_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='received_messages')
    application = models.ForeignKey(to='application.Application', on_delete=models.CASCADE, related_name='group_messages')
    message = models.TextField(max_length=MAX_MESSAGE_LENGTH)
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    created_time = models.DateTimeField(auto_now_add=True)

    class MessageCheckStatus(Enum):
        '''
        进行数据检查的状态结果
        '''

        MESSAGE_TOO_LOOG = 'message too long'
        MESSAGE_CHAR_ERROR = 'unusable char in message (possibly {{ or }})'
        TITLE_TOO_LOOG = 'title too long'
        TITLE_CHAR_ERROR = 'unusable char in message (possibly {{ or }})'
        SUCCEED = 'succeed'

    def to_dict(self) -> Dict[str, Any]:
        '''
        将本对象的信息化为一个字典对象返回
        '''

        return {
            JsonResponseDictConst.FROM_USERNAME: self.from_user.username,
            JsonResponseDictConst.TO_USERNAME: self.to_user.username,
            JsonResponseDictConst.TITLE: self.title,
            JsonResponseDictConst.CREATED_TIME: self.created_time,
            JsonResponseDictConst.MESSAGE: self.message,
        }

    def send_mail(self) -> bool:
        '''
        阻塞式进行邮件发送

        返回值表示是否发送成功
        '''

        if not self.to_user.email:
            return False

        html_message = transform_html(self.message)
        html_title = transform_html(self.title)
        from_username = transform_html(self.from_user.username)
        application_name = transform_html(self.application.name)
        from_avatar = get_user_info(self.from_user).get_avatar_url()

        text_content = EMAIL_TEXT_CONTENT.replace(
            BackendConst.MessageEmailPlaceHolder.MESSAGE,
            self.message
        ).replace(
            BackendConst.MessageEmailPlaceHolder.FROM_USERNAME,
            from_username
        ).replace(
            BackendConst.MessageEmailPlaceHolder.APPLICATION_NAME,
            application_name
        ).replace(
            BackendConst.MessageEmailPlaceHolder.TITLE,
            self.title
        )

        html_content = EMAIL_HTML_CONTENT.replace(
            BackendConst.MessageEmailPlaceHolder.APPLICATION_NAME,
            application_name
        ).replace(
            BackendConst.MessageEmailPlaceHolder.FROM_USERNAME,
            from_username
        ).replace(
            BackendConst.MessageEmailPlaceHolder.FROM_AVATAR,
            BackendConst.BACKEND_HOST + from_avatar
        ).replace(
            BackendConst.MessageEmailPlaceHolder.MESSAGE,
            html_message
        ).replace(
            BackendConst.MessageEmailPlaceHolder.TITLE,
            html_title
        )

        email = EmailMultiAlternatives('通用权限平台用户信息', text_content, settings.DEFAULT_FROM_EMAIL, [self.to_user.email])
        email.attach_alternative(html_content, 'text/html')

        return bool(email.send())

    @classmethod
    def create_message(cls, from_user: User, to_user: User, message: str, application, title: Union[str, None] = None, 
        auto_mail: bool = False) -> Tuple[Union['UserMessage', None], 'UserMessage.MessageCheckStatus']:
        '''
        创建一个新的信息，可以用auto_mail参数指定是否自动通过邮箱发送

        application: Application
        '''

        check_status = cls.general_check(message=message, title=title)
        if check_status != cls.MessageCheckStatus.SUCCEED:
            return None, check_status

        if title is None or title == '':
            title = '无标题'

        new_message = cls.objects.create(
            to_user=to_user,
            from_user=from_user,
            message=message,
            application=application,
            title=title
        )

        if auto_mail:
            send_message(new_message)

        return new_message, check_status

    @classmethod
    def general_check(cls, message: str, title: Union[str, None] = None) -> 'UserMessage.MessageCheckStatus':
        '''
        创建新消息的时候的通用检查选项
        '''

        if len(message) > cls.MAX_MESSAGE_LENGTH:
            return cls.MessageCheckStatus.MESSAGE_TOO_LOOG
        if '{{' in message or '}}' in message:
            return cls.MessageCheckStatus.MESSAGE_CHAR_ERROR

        if title is not None:
            if len(title) > cls.MAX_TITLE_LENGTH:
                return cls.MessageCheckStatus.TITLE_TOO_LOOG
            if '{{' in title or '}}' in title:
                return cls.MessageCheckStatus.TITLE_CHAR_ERROR

        return cls.MessageCheckStatus.SUCCEED
