import datetime

from typing import Any, Dict, Union, Tuple, List
from pytz import UTC
from django.db import models
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from application_token.models import ApplicationToken
from application_auth.models import ApplicationAuth
from application_user.models import ApplicationUser
from application_role.models import ApplicationRole
from user_app_relation.models import UserApplicationRelation
from user_info.views import get_user_info
from utils.models import SetModelStatus
from utils.const import BackendConst, JsonResponseDictConst, RequestFieldConst

# Create your models here.

User = get_user_model()


class Application(models.Model):
    '''
    App类
    - tokens: 本应用所有关联的token
    - name: App的名字
    - key: App的key
    - description: App简介
    - user: 拥有本App的开发者用户
    - application_users: 含有的所有用户
    - application_roles: 含有的所有角色
    - application_auths: 含有的所有权限
    - created_time: 创建时间
    - shared_users: 被共享给的用户
    - user_relations: 和平台用户的关系（用于关联自己和shared_users）
    - group_messages: 用户组的用户之间的提醒信息
    '''

    MAX_NAME_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 1000
    MAX_KEY_LENGTH = 100
    KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ-'

    name = models.CharField(max_length=MAX_NAME_LENGTH)
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='applications')
    shared_users = models.ManyToManyField(to=User, related_name='shared_applications', through=UserApplicationRelation)
    created_time = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=MAX_KEY_LENGTH)

    class ApplicationCheckStatus:
        '''
        更改或创建Application类对象的时候的参数检查结果
        '''

        KEY_CONFLICT = 'key conflict'
        NAME_TOO_LONG = 'name too long'
        NAME_CHAR_ERROR = 'unusable char in name (possibly {{ or }})'
        KEY_TOO_LONG = 'key too long'
        DESCRIPTION_TOO_LONG = 'description too long'
        NAME_EMPTY = 'name empty'
        KEY_EMPTY = 'key empty'
        KEY_CHAR_ERROR = 'unusable char in key'
        SUCCEED = 'succeed'

    def __str__(self) -> str:
        return str(self.name)

    def to_dict(self, max_token_number: int = 20, token_access: Union[ApplicationToken.ApplicationAccessStatus, int, None] 
        = None, user: Union[User, None] = None) -> Union[Dict[str, Any], None]:
        '''
        返回App的基本信息

        通过token_access传入当前接触这个App使用的token的权限

        如果token_access没传，则设为默认（如果指定了user，采用user的权限；否则采用最高权限）
        '''

        return_dict = {
            'name': self.name,
            'created_user': self.user.username,
            'created_time': self.created_time,
            'description': self.description,
            JsonResponseDictConst.KEY: self.key
        }

        if user is not None:
            user_access = self.get_user_access(user)
            return_dict.update({
                JsonResponseDictConst.ACCESS: user_access.value,
            })

            if token_access is None:
                token_access = user_access.value

        if token_access is None:
            token_access = ApplicationToken.ApplicationAccessStatus.ALL

        try:
            token_access = ApplicationToken.ApplicationAccessStatus(token_access)
        except ValueError:
            return None

        possible_tokens = self.get_tokens(token_access=token_access)
        if possible_tokens is None:
            return return_dict

        token_list = [token.to_dict() for token in possible_tokens[: max_token_number]]
        token_list.sort(key=lambda token_dict: token_dict[JsonResponseDictConst.ACCESS])

        return_dict.update({
            'tokens': token_list,
        })

        return return_dict

    def get_user_group(self) -> List[Dict[str, Any]]:
        '''
        获得已经注册好权限的排序后的用户组
        '''

        return_list = []

        for user in self.shared_users.all():
            user_dict = get_user_info(user).to_dict()
            user_dict.update({
                JsonResponseDictConst.ACCESS: self.get_user_access(user).value,
            })
            return_list += [user_dict]

        create_user_dict = get_user_info(self.user).to_dict()
        create_user_dict.update({
            JsonResponseDictConst.ACCESS: UserApplicationRelation.UserAccessStatus.CREATOR.value,
        })
        return_list += [create_user_dict]

        return_list.sort(key=lambda user_dict: user_dict[JsonResponseDictConst.ACCESS])
        return return_list

    def get_user_access(self, user: User) -> UserApplicationRelation.UserAccessStatus:
        '''
        获得该用户对本App的访问权限
        '''

        return UserApplicationRelation.get_access(self, user)

    def share(self, to_user: User, access: Union[UserApplicationRelation.UserAccessStatus, int] 
        = UserApplicationRelation.UserAccessStatus.ADMIN) -> bool:
        '''
        以指定权限共享给指定的用户，返回值表示是否成功共享
        '''

        possible_relation = UserApplicationRelation.share(application=self, user=to_user, access=access)
        return (possible_relation is not None)

    def unshare(self, to_user: User) -> bool:
        '''
        取消对某个用户的共享

        返回值表示是否成功操作
        '''

        return UserApplicationRelation.unshare(self, to_user)

    def change_detail(self, user: User, name: Union[str, None] = None, description: Union[str, None] = None,
        key: Union[str, None] = None) -> Union['Application.ApplicationCheckStatus']:
        '''
        更改当前Application的详情，返回更改状态（不是SUCCEED都是更改失败）
        '''

        cls = type(self)

        check_result = cls.general_check(user, name, description, key=key, for_change=True, application=self)
        if check_result != cls.ApplicationCheckStatus.SUCCEED:
            return check_result

        if name is not None:
            name = str(name)
            self.name = name
        if description is not None:
            description = str(description)
            self.description = description
        if key is not None:
            key = str(key)
            self.key = key
        self.save()

        return cls.ApplicationCheckStatus.SUCCEED

    def get_tokens(self, token_access: Union[ApplicationToken.ApplicationAccessStatus, int], exact_access = False) -> Union[QuerySet[ApplicationToken], None]:
        '''
        调用此函数，若exact_access为False，获得以权限为token_access的token视角下得到的App的所有可见权限；否则获得该权限的所有token

        与直接操作tokens不同，调用这个函数的时候会自动删除过期的token，并如果没有token会自动创建一个token
        '''

        try:
            token_access = ApplicationToken.ApplicationAccessStatus(token_access)
        except ValueError:
            return None

        self.tokens.filter(dead_time__lte=datetime.datetime.now(UTC)).delete()

        if not self.tokens.filter(access=token_access.value).exists():
            self.tokens.add(ApplicationToken.create_token(self, token_access))

        if exact_access:
            return ApplicationToken.objects.filter(access=token_access.value, application=self)

        if token_access == ApplicationToken.ApplicationAccessStatus.ALL:
            return self.tokens.all()
        elif token_access == ApplicationToken.ApplicationAccessStatus.ADMIN:
            return ApplicationToken.objects.filter(access__gte=token_access.value, application=self)
        else:
            return ApplicationToken.objects.filter(access=token_access.value, application=self)

    def create_token(self, token_access: ApplicationToken.ApplicationAccessStatus 
        = ApplicationToken.ApplicationAccessStatus.ALL) -> ApplicationToken:
        '''
        新建指定权限的token
        '''

        return ApplicationToken.create_token(self, access=token_access)

    def create_auth(self, key: str, name: Union[str, None] = None, description: str = ''
        ) -> Tuple[SetModelStatus, Union[ApplicationAuth, None]]:
        '''
        新建App中的权限
        '''

        return ApplicationAuth.create_application_auth(self, key=key, name=name, description=description)
        
    def create_role(self, key: str, name: Union[str, None] = None, description: str = ''
        ) -> Tuple[SetModelStatus, Union[ApplicationRole, None]]:
        '''
        新建App中的角色
        '''

        return ApplicationRole.create_application_role(self, key=key, name=name, description=description)
             
    def create_user(self, key: str, name: Union[str, None] = None, description: str = ''
        ) -> Tuple[SetModelStatus, Union[ApplicationUser, None]]:
        '''
        新建App中的用户
        '''
        
        return ApplicationUser.create_application_user(self, key=key, name=name, description=description)

    def create_type(self, operate_type: RequestFieldConst.OperateType, key: str, name: Union[str, None] = None, description: str = ''
        ) -> Tuple[SetModelStatus, Union[None, ApplicationAuth, ApplicationRole, ApplicationUser]]:
        '''
        新建一个通过operate_type指定的ApplicationXXX类型对象

        返回的是一个元组，可以用第一个参数判断是否成功以及失败原因，第二个参数才是结果
        '''

        if operate_type == RequestFieldConst.OperateType.USER:
            return self.create_user(key, name, description)
        elif operate_type == RequestFieldConst.OperateType.AUTH:
            return self.create_auth(key, name, description)
        elif operate_type == RequestFieldConst.OperateType.ROLE:
            return self.create_role(key, name, description)
        else:
            return (SetModelStatus.UNEXPECTED_FAIL, None)

    def create_child_type(self, operate_type: RequestFieldConst.OperateType, key: str, parent_key: str, name: Union[str, None] = None, 
        description: str = '') -> Tuple[SetModelStatus, Union[None, ApplicationAuth, ApplicationRole, ApplicationUser]]:
        '''
        与create_type类似，但是需要提供parent_key指定父对象
        '''

        if operate_type == RequestFieldConst.OperateType.AUTH:
            parent_auth= self.application_auths.filter(key=parent_key).first()
            if parent_auth is None:
                return (SetModelStatus.NO_PARENT_OBJECT, None)
            return parent_auth.create_child_auth(key, name, description)
        else:
            return (SetModelStatus.UNEXPECTED_FAIL, None)

    @classmethod
    def get_application_by_token_string(cls, token_string: str, app_key: str
        ) -> Tuple[Union['Application', None], Union[ApplicationToken.ApplicationAccessStatus, None]]:
        '''
        通过token和app_key的内容找到对应ApplicationToken关联的Application

        返回的是一个二元组

        如果没有符合传入内容的ApplicationToken或者它已经过期（过期的话自动删除），第一个参数就会返回None，否则返回找到的Application

        第二个参数指示该token的权限
        '''

        possible_token = ApplicationToken.objects.filter(content=token_string).first()
        if possible_token is None or (not possible_token.check_self()) or possible_token.application.key != app_key:
            return None, None
        return possible_token.application, ApplicationToken.ApplicationAccessStatus(possible_token.access)

    @classmethod
    def create_application_for_user(cls, user: User, name: str, description: str = '', app_key: Union[str, None] = None, 
        default_auths: Union[List[Dict[str, Any]], None] = None, with_status: bool = False
        ) -> Union[Union['Application', None], Tuple[Union['Application', None], Union['Application.ApplicationCheckStatus', None]]]:
        '''
        指定的新建App方法，不要用Application.objects.create
        '''

        if app_key is None:
            app_key = name

        check_status = cls.general_check(user=user, name=name, description=description, key=app_key)
        if check_status != cls.ApplicationCheckStatus.SUCCEED:
            if with_status:
                return (None, check_status)
            else:
                return None

        if default_auths is None:
            default_auths = [
                {
                    BackendConst.PARAM_KEY: 'menu',
                    BackendConst.PARAM_NAME: '菜单',
                    BackendConst.PARAM_DESCRIPTION: '菜单权限',
                },
                {
                    BackendConst.PARAM_KEY: 'detail',
                    BackendConst.PARAM_NAME: '详情',
                    BackendConst.PARAM_DESCRIPTION: '详情权限',
                },
                {
                    BackendConst.PARAM_KEY: 'manage',
                    BackendConst.PARAM_NAME: '管理',
                    BackendConst.PARAM_DESCRIPTION: '管理权限',
                },
            ]

        return_application = cls.objects.create(
            user=user,
            name=name,
            description=description,
            key=app_key
        )

        for auth in default_auths:
            return_application.create_auth(**auth)

        if with_status:
            return (return_application, cls.ApplicationCheckStatus.SUCCEED)
        else:
            return return_application

    @classmethod
    def general_check(cls, user: User, name: Union[str, None] = None, description: Union[str, None] = None, 
        key: Union[str, None] = None, for_change: bool = False, application: Union[None, 'Application'] = None) -> Union['Application.ApplicationCheckStatus']:
        '''
        对传入参数做一些检查
        '''

        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-branches

        if name is not None:
            name = str(name)
            if name == '':
                return cls.ApplicationCheckStatus.NAME_EMPTY
            if len(name) > cls.MAX_NAME_LENGTH:
                return cls.ApplicationCheckStatus.NAME_TOO_LONG
            if '{{' in name or '}}' in name:
                return cls.ApplicationCheckStatus.NAME_CHAR_ERROR

        if key is not None:
            key = str(key)
            if key == '':
                return cls.ApplicationCheckStatus.KEY_EMPTY
            if len(key) > cls.MAX_KEY_LENGTH:
                return cls.ApplicationCheckStatus.KEY_TOO_LONG
            if not for_change:
                if cls.objects.filter(key=key, user=user).exists():
                    return cls.ApplicationCheckStatus.KEY_CONFLICT
            else:
                if key != application.key and cls.objects.filter(key=key, user=user).exists():
                    return cls.ApplicationCheckStatus.KEY_CONFLICT

            for char in key:
                if not char in cls.KEY_CHARS:
                    return cls.ApplicationCheckStatus.KEY_CHAR_ERROR

        if description is not None:
            description = str(description)
            if len(description) > cls.MAX_DESCRIPTION_LENGTH:
                return cls.ApplicationCheckStatus.DESCRIPTION_TOO_LONG

        return cls.ApplicationCheckStatus.SUCCEED
