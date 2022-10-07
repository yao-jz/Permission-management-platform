from typing import Any, Dict, Set, Tuple, Union
from django.db import models
from django.db.models.query import QuerySet

from utils.const import RequestFieldConst, JsonResponseDictConst
from utils.models import SetModelStatus
from utils.views import general_set_model_check

# Create your models here.


class ApplicationAuth(models.Model):
    '''
    权限类
    - key: 区分不同权限的字段，仅接受英文、下划线、横杠、数字组合而成的字段
    - name: 别名，用来显示给开发者用户看的
    - application: 从属于哪个App
    - description: 对这个权限的简短说明
    - roles: 拥有本权限的所有角色
    - parent_auth: 父权限
    - child_auths: 所有子权限
    - time: 创建时间
    '''

    MAX_KEY_LENGTH = 40
    MAX_NAME_LENGTH = 40
    MAX_DESCRIPTION_LENGTH = 200
    KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ-'

    key = models.CharField(max_length=MAX_KEY_LENGTH)
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    application = models.ForeignKey(to='application.Application', on_delete=models.CASCADE, related_name='application_auths')
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH, blank=True)
    parent_auth = models.ForeignKey(to='self', null=True, blank=True, related_name='child_auths', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            JsonResponseDictConst.AUTH_NAME: self.name,
            JsonResponseDictConst.AUTH_KEY: self.key,
            JsonResponseDictConst.CREATED_TIME: self.time,
            JsonResponseDictConst.PARENT_AUTH: self.get_parent_auth_dict(),
            JsonResponseDictConst.CHILD_AUTHS: [item.to_dict() for item in self.child_auths.all()]
        }

    def get_parent_auth_dict(self) -> Dict[str, str]:
        if not self.parent_auth:
            return dict()

        return {
            JsonResponseDictConst.AUTH_NAME: self.parent_auth.name,
            JsonResponseDictConst.AUTH_KEY: self.parent_auth.key,
        }

    def get_users(self) -> set:
        '''
        获得所有关联的用户

        需要通过role作中间件来获取，效率较低，所以谨慎调用

        -> Set[ApplicationUser]
        '''

        return_set = set()
        for role in self.roles.all():
            return_set.update(set(role.users.all()))
        return return_set
        
    def get_objects_of_type(self, operate_type: RequestFieldConst.OperateType) -> set:
        '''
        三个ApplicationXXX都有的方法，适用于show API
        '''

        if operate_type == RequestFieldConst.OperateType.ROLE:
            return set(self.roles.all())
        elif operate_type == RequestFieldConst.OperateType.USER:
            return self.get_users()
        else:
            return set()

    def get_childest_set(self) -> Set['ApplicationAuth']:
        '''
        获得本权限的所有下属叶子权限的集合
        '''

        return_set = set()
        for child_auth in self.child_auths.all():
            return_set.update(child_auth.get_childest_set())

        return return_set if return_set else {self}

    def create_child_auth(self, key: str, name: Union[str, None] = None, description: str = '') -> Tuple[SetModelStatus, Union['ApplicationAuth', None]]:
        '''
        新建一个子权限，然后把自身所有关联角色全部转移到子权限
        '''

        cls = type(self)

        if name is None:
            name = key

        general_check_status = general_set_model_check(cls, key, name, description)
        if general_check_status != SetModelStatus.SUCCEED:
            return (general_check_status, None)

        if cls.objects.filter(application=self.application, key=key).exists():
            return (SetModelStatus.KEY_ALREADY_EXISTS, None)

        child_auth = cls.objects.create(
            application = self.application,
            key = key,
            name = name,
            parent_auth = self,
            description = description
        )

        for role in self.roles.all():
            self.roles.remove(role)
            child_auth.roles.add(role)

        return (SetModelStatus.SUCCEED, child_auth)

    @classmethod
    def create_application_auth(cls, application, key: str, name: Union[str, None] = None, description: str = '') -> Tuple[SetModelStatus, Union['ApplicationAuth', None]]:
        '''
        application: Application
        '''

        if name is None:
            name = key
        
        general_check_status = general_set_model_check(cls, key, name, description)
        if general_check_status != SetModelStatus.SUCCEED:
            return (general_check_status, None)
        elif cls.objects.filter(application = application, key = key).exists():
            return (SetModelStatus.KEY_ALREADY_EXISTS, None)

        return (SetModelStatus.SUCCEED, cls.objects.create(
            application = application,
            key = key,
            name = name,
            description = description
        ))
