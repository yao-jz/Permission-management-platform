from typing import Dict, Any, Iterable, Union, Tuple
from django.db import models

from application_role.models import ApplicationRole
from user_role_relation.models import UserRoleRelation
from utils.const import RequestFieldConst, JsonResponseDictConst
from utils.models import SetModelStatus
from utils.views import general_set_model_check

# Create your models here.


class ApplicationUser(models.Model):
    '''
    用户类
    - key: 区分不同用户的字段，仅接受英文、下划线、横杠、数字组合而成的字段
    - name: 用户别名，用来展示给开发者用户看的
    - roles: 用户从属的所有角色
    - application: 从属于哪个App
    - description: 简要说明
    - time: 创建时间
    - role_relations: 反向查询角色关联类
    '''

    MAX_KEY_LENGTH = 40
    MAX_NAME_LENGTH = 40
    MAX_DESCRIPTION_LENGTH = 200
    KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ-'

    key = models.CharField(max_length=MAX_KEY_LENGTH)
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    application = models.ForeignKey(to='application.Application', on_delete=models.CASCADE, related_name='application_users')
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH, blank=True)
    roles = models.ManyToManyField(to=ApplicationRole, related_name='users', through=UserRoleRelation)
    time = models.DateTimeField(auto_now_add=True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            JsonResponseDictConst.USER_NAME: self.name,
            JsonResponseDictConst.USER_KEY: self.key,
            JsonResponseDictConst.CREATED_TIME: self.time
        }

    def _attach_application_role(self, role: ApplicationRole) -> None:
        assert(self.application == role.application)

        UserRoleRelation.attach(self, role)

    def attach_application_roles(self, roles: Iterable[ApplicationRole]) -> None:
        '''
        关联用户的角色
        '''
        
        for role in roles:
            self._attach_application_role(role)

    def get_auths(self) -> set:
        '''
        获得拥有的所有权限

        需要通过role作中间件来获取，效率较低，所以谨慎调用

        -> Set[ApplicationAuth]
        '''

        return_set = set()

        for role in self.roles.all():
            return_set.update(set(role.auths.all()))

        return return_set
        
    def get_objects_of_type(self, operate_type: RequestFieldConst.OperateType) -> set:
        '''lly you will hit the same problem as OP wrote. To solve it, follow these steps:


        三个ApplicationXXX都有的方法，适用于show API
        '''
        if operate_type == RequestFieldConst.OperateType.AUTH:
            return self.get_auths()
        elif operate_type == RequestFieldConst.OperateType.ROLE:
            return set(UserRoleRelation.get_roles(self))
        else:
            return set()

    @classmethod
    def create_application_user(cls, application, key: str, name: Union[str, None] = None, description: str = '') -> Tuple[SetModelStatus, Union['ApplicationUser', None]]:
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

        return_user = cls.objects.create(
            application = application,
            key = key,
            name = name,
            description = description
        )

        return (SetModelStatus.SUCCEED, return_user)
