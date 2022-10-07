from enum import Enum
from typing import Union
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class UserApplicationRelation(models.Model):
    '''
    平台用户和App之间的关系类
    - user: 关联的平台用户
    - application: 关联的App
    - access: 用户对App的权限
    '''

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='application_relations')
    application = models.ForeignKey(to='application.Application', on_delete=models.CASCADE, related_name='user_relations')
    access = models.IntegerField()

    class UserAccessStatus(Enum):
        '''
        平台用户对App的控制权限

        基本和token对App的权限语义相同
        '''

        CREATOR = 0
        ADMIN = 1
        ADD = 2
        EDIT = 3
        SEE = 4
        NO = 5

        def __str__(self) -> str:

            # pylint: disable=too-many-return-statements

            cls = type(self)
            if self == cls.CREATOR:
                return 'creator'
            if self == cls.ADMIN:
                return 'admin'
            if self == cls.ADD:
                return 'add'
            if self == cls.EDIT:
                return 'edit'
            if self == cls.SEE:
                return 'see'
            if self == cls.NO:
                return 'no'
            return 'unknow'

        def check_access(self, access_needed: Union[int, 'UserApplicationRelation.UserAccessStatus']) -> bool:
            '''
            检查自身权限是否比需要的权限高
            '''

            # pylint: disable=comparison-with-callable

            if isinstance(access_needed, type(self)):
                return self.value <= access_needed.value
            else:
                return self.value <= int(access_needed)

    @classmethod
    def share(cls, application, user: User, access: Union['UserApplicationRelation.UserAccessStatus', int]
        ) -> Union['UserApplicationRelation', None]:
        '''
        把App分享给用户

        application: Application
        '''

        if application.user == user:
            return None

        if not isinstance(access, cls.UserAccessStatus):
            try:
                access = cls.UserAccessStatus(int(access))
            except ValueError:
                return None

        if access == UserApplicationRelation.UserAccessStatus.CREATOR:
            return None

        possible_relation = cls.objects.filter(user=user, application=application).first()
        if possible_relation is not None:
            possible_relation.access = access.value
            possible_relation.save()
            return possible_relation

        return cls.objects.create(
            application = application,
            user = user,
            access = access.value
        )

    @classmethod
    def unshare(cls, application, user: User) -> bool:
        '''
        取消用户和App间的共享关系，返回值表示是否成功

        application: Application
        '''

        if application.user == user:
            return False

        possible_relation = cls.objects.filter(user=user, application=application)
        if not possible_relation.exists():
            return False

        possible_relation.delete()
        return True

    @classmethod
    def get_access(cls, application, user: User) -> 'UserApplicationRelation.UserAccessStatus':
        '''
        获得指定的App和用户之间的权限关系

        application: Application
        '''

        if user == application.user:
            return cls.UserAccessStatus.CREATOR

        possible_relation = cls.objects.filter(user = user, application = application).first()
        if possible_relation is None:
            return cls.UserAccessStatus.NO
            
        return cls.UserAccessStatus(possible_relation.access)
