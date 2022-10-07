import datetime

from typing import Union
from django.db import models
from pytz import UTC

# Create your models here.


class UserRoleRelation(models.Model):
    '''
    App用户和角色的关联类
    - application_user: 关联的用户
    - application_role: 关联的角色
    - created_time: 关系创建时间
    - dead_time: 关系失效时间
    - forever: 是否是永久关系
    '''

    DEFAULT_TIME_OUT = datetime.timedelta(weeks=1)

    application_user = models.ForeignKey(to='application_user.ApplicationUser', on_delete=models.CASCADE, related_name='role_relations')
    application_role = models.ForeignKey(to='application_role.ApplicationRole', on_delete=models.CASCADE, related_name='user_relations')

    created_time = models.DateTimeField(auto_now_add=True)
    dead_time = models.DateTimeField()
    forever = models.BooleanField()

    @classmethod
    def attach(cls, user, role, time_out: Union[None, int] = None) -> Union[None, 'UserRoleRelation']:
        '''
        关联用户和角色，如果成功关联则返回使用的关联类变量，否则返回None

        user: ApplicationUser, role: ApplicationRole
        '''

        if isinstance(time_out, int):
            time_out = datetime.timedelta(seconds=time_out)
        else:
            time_out = None

        possible_relations = cls.objects.filter(application_user=user, application_role=role)
        if possible_relations.exists():
            existed_relation = possible_relations.first()
            if time_out is None:
                existed_relation.forever = True
            else:
                existed_relation.dead_time = datetime.datetime.now(UTC) + time_out
                existed_relation.forever = False
            existed_relation.save()
            return existed_relation
        
        return cls.objects.create(
            application_user=user,
            application_role = role,
            dead_time = datetime.datetime.now(UTC) + (cls.DEFAULT_TIME_OUT if time_out is None else time_out),
            forever = (time_out is None)
        )

    @classmethod
    def detach(cls, user, role) -> None:
        '''
        解联用户和角色，无论原来是否有这个关系都静默执行

        user: ApplicationUser, role: ApplicationRole
        '''

        cls.objects.filter(application_user=user, application_role=role).delete()

    @classmethod
    def get_roles(cls, user) -> set:
        '''
        获得用户关联的所有角色

        user: ApplicationUser
        '''

        cls.objects.filter(application_user=user, forever=False, dead_time__lte=datetime.datetime.now(UTC)).delete()

        return_set = set()
        for relation in cls.objects.filter(application_user=user):
            return_set.update({relation.application_role})

        return return_set

    @classmethod
    def get_users(cls, role) -> set:
        '''
        获得角色关联的所有用户

        role: ApplicationRole
        '''

        cls.objects.filter(application_role=role, forever=False, dead_time__lte=datetime.datetime.now(UTC)).delete()

        return_set = set()
        for relation in cls.objects.filter(application_role=role):
            return_set.update({relation.application_user})

        return return_set
