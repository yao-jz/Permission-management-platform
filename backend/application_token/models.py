import datetime

from typing import Any, Dict, Union
from enum import Enum
from pytz import UTC
from django.db import models

from utils.const import JsonResponseDictConst
from utils.views import generate_random_str

# Create your models here.


class ApplicationToken(models.Model):
    '''
    App的token鉴权辅助类
    - content: 存储的原始内容
    - created_time: 存入的时间
    - dead_time: 若forever为False，表示销毁时间
    - application: 关联的应用
    - forever: 是否是永久token
    - access: 对关联的App的权限
    '''

    TOKEN_LENGTH = 30
    DEFAULT_TIME_OUT = datetime.timedelta(weeks=1)
    TOKEN_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ-'

    content = models.CharField(max_length=TOKEN_LENGTH)
    created_time = models.DateTimeField(auto_now_add=True)
    dead_time = models.DateTimeField()
    application = models.ForeignKey(to='application.Application', on_delete=models.CASCADE, related_name='tokens')
    forever = models.BooleanField(default=False)
    access = models.IntegerField()

    class ApplicationAccessStatus(Enum):
        '''
        token对App的控制权限
        '''

        ALL = 0  # 所有权限，与创建者相同，包括删除本token与删除App
        ADMIN = 1  # 进行任何管理，可以分发下层的更多token，但是不能删除App
        ADD = 2  # 可以添加和删除用户，角色，权限
        EDIT = 3  # 可以编辑App的内部逻辑（即用户，角色，权限之间的关联逻辑）
        SEE = 4  # 只可以观看，不可以编辑

        def __str__(self) -> str:
            cls = type(self)
            if self == cls.ALL:
                return 'all'
            elif self == cls.ADMIN:
                return 'admin'
            elif self == cls.ADD:
                return 'add'
            elif self == cls.EDIT:
                return 'edit'
            elif self == cls.SEE:
                return 'see'
            else:
                return 'unknow'

        def check_access(self, access_needed: Union[int, 'ApplicationToken.ApplicationAccessStatus']) -> bool:
            '''
            检查当前拥有的权限是否能够满足所需的权限要求

            若能够覆盖所需权限，返回True，否则返回False
            '''
            if isinstance(access_needed, type(self)):
                return self.value <= access_needed.value  # pylint: disable=W0143
            else:
                return self.value <= int(access_needed)  # pylint: disable=W0143

    def __str__(self) -> str:
        return f'(created at {self.created_time} ({"forever" if self.forever else self.dead_time})){self.content}'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'content': self.content,
            'created_time': self.created_time,
            'dead_time': self.dead_time if not self.forever else 'forever',
            JsonResponseDictConst.ACCESS: self.access,
        }

    def check_self(self) -> bool:
        '''
        检查自身是否过期，若过期则调用自己的delete函数，并返回False；否则返回True
        '''

        if not self.forever and self.dead_time <= datetime.datetime.now(UTC):
            self.delete()
            return False
        else:
            return True

    @classmethod
    def create_token(cls, application, access: Union['ApplicationToken.ApplicationAccessStatus', int] = 0) -> 'ApplicationToken':
        '''
        参数application需要是Application类型
        '''

        token_string = generate_random_str(cls.TOKEN_LENGTH, cls.TOKEN_CHARS)
        while True:
            possible_application_token = cls.objects.filter(content=token_string).first()
            if possible_application_token is None:
                break
            if not possible_application_token.forever and datetime.datetime.now(UTC) >= possible_application_token.dead_time:
                possible_application_token.delete()
                break
            token_string = generate_random_str(cls.TOKEN_LENGTH, cls.TOKEN_CHARS)

        application_token = cls.objects.create(
            content = token_string,
            application = application,
            dead_time = datetime.datetime.now(UTC) + cls.DEFAULT_TIME_OUT,
            access = access.value if isinstance(access, cls.ApplicationAccessStatus) else int(access)
        )

        return application_token

    @classmethod
    def change_access(cls, token_string: str, new_access: Union['ApplicationToken.ApplicationAccessStatus', int]) -> bool:
        '''
        改变对应token对应的权限，返回值指示是否成功进行改变
        '''

        possible_tokens = cls.objects.filter(content=token_string)
        if not possible_tokens.exists():
            return False

        token = possible_tokens.first()
        if not token.check_self():
            return False

        token.access = new_access.value if isinstance(new_access, cls.ApplicationAccessStatus) else new_access
        token.save()

        return True
