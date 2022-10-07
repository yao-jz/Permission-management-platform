from typing import Any, Dict, Iterable, Tuple, Union
from django.db import models

from application_auth.models import ApplicationAuth
from user_role_relation.models import UserRoleRelation
from utils.models import SetModelStatus
from utils.views import general_set_model_check
from utils.const import RequestFieldConst, JsonResponseDictConst

# Create your models here.


class ApplicationRole(models.Model):
    '''
    角色类
    - key: 区分不同角色的字段，仅接受英文、下划线、横杠、数字组合而成的字段
    - name: 别名，用来显示给开发者用户看的
    - application: 从属于哪个App
    - auths: 本类角色拥有的权限
    - description: 对这个角色的简短说明
    - users: 扮演本角色的所有用户
    - time: 创建时间
    - user_relations: 反向查询用户关联类
    '''

    MAX_KEY_LENGTH = 40
    MAX_NAME_LENGTH = 40
    MAX_DESCRIPTION_LENGTH = 200
    KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ-'

    key = models.CharField(max_length=MAX_KEY_LENGTH)
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    application = models.ForeignKey(to='application.Application', on_delete=models.CASCADE, related_name='application_roles')
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH, blank=True)
    auths = models.ManyToManyField(to=ApplicationAuth, related_name='roles')
    time = models.DateTimeField(auto_now_add=True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            JsonResponseDictConst.ROLE_NAME: self.name,
            JsonResponseDictConst.ROLE_KEY: self.key,
            JsonResponseDictConst.CREATED_TIME: self.time
        }

    def _detach_application_auth(self, auth: ApplicationAuth) -> None:
        if auth.application != self.application:
            return

        if auth in self.auths.all():
            self.auths.remove(auth)

    def detach_application_auths(self, auths: Iterable[ApplicationAuth]) -> None:
        '''
        静默删除auths中的每个对象的关联，不会抛出异常
        '''

        for auth in auths:
            self._detach_application_auth(auth)

    def attach_application_auths(self, auths: Iterable[ApplicationAuth]) -> None:
        '''
        需要确保auths中对象都和本角色对象关联上同一个App，否则会抛出异常
        '''

        for auth in auths:
            self._attach_application_auth(auth)

    def _attach_application_auth(self, auth: ApplicationAuth) -> None:
        assert(auth.application == self.application)

        if auth not in self.auths.all():
            self.auths.add(auth)

    def _detach_application_user(self, user) -> None:
        '''
        user: ApplicationUser | Tuple[ApplicationUser, ...]
        '''

        if isinstance(user, tuple):
            if len(user) < 1:
                return
            user = user[0]

        assert(self.application == user.application)

        UserRoleRelation.detach(user, self)

    def detach_application_users(self, users: Iterable) -> None:
        '''
        users: Iterable[ApplicationUser | Tuple[ApplicationUser, ...]]

        对于users中每一项，如果它是元组，则认为第一个为user
        '''

        for user in users:
            self._detach_application_user(user)

    def _attach_application_user(self, user) -> None:
        '''
        user: ApplicationUser | Tuple[ApplicationUser, int | None]
        '''

        if isinstance(user, tuple):
            if len(user) < 2:
                return
            time_out = user[1]
            user = user[0]
        else:
            time_out = None

        assert(self.application == user.application)

        UserRoleRelation.attach(user, self, time_out)

    def attach_application_users(self, users: Iterable) -> None:
        '''
        users: Iterable[ApplicationUser | Tuple[ApplicationUser, int | None]]

        对于users中每一项，如果它是元组，则认为第一个为user，第二个（int）为关联时限（秒）
        '''

        for user in users:
            self._attach_application_user(user)

    def get_objects_of_type(self, operate_type: RequestFieldConst.OperateType) -> set:
        '''
        三个ApplicationXXX都有的方法，适用于show API
        '''

        if operate_type == RequestFieldConst.OperateType.AUTH:
            return set(self.auths.all())
        elif operate_type == RequestFieldConst.OperateType.USER:
            return UserRoleRelation.get_users(self)
        else:
            return set()

    @classmethod
    def create_application_role(cls, application, key: str, name: Union[str, None] = None, description: str = '') -> Tuple[SetModelStatus, Union['ApplicationRole', None]]:
        '''
        application: Application
        '''

        if name is None:
            name = key

        general_check_status = general_set_model_check(cls, key, name, description)
        if general_check_status != SetModelStatus.SUCCEED:
            return (general_check_status, None)
        elif cls.objects.filter(key=key, application=application).exists():
            return (SetModelStatus.KEY_ALREADY_EXISTS, None)

        return_role = cls.objects.create(
            application = application,
            key = key,
            name = name,
            description = description
        )

        return (SetModelStatus.SUCCEED, return_role)
