import shutil
import os

from typing import Any, Dict, Union, Tuple
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files import uploadedfile

from utils.const import BackendConst, JsonResponseDictConst

# Create your models here.

User = get_user_model()


class UserInfo(models.Model):
    '''
    用户信息存储类
    - user: 关联的用户
    - avatar: 用户头像，存于MEDIA_DIR/AVATAR_DIR/<user_id>.png
    '''

    AVATAR_DIR_NAME = 'avatars'
    AVATAR_DIR = os.path.join(settings.MEDIA_ROOT, AVATAR_DIR_NAME)

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='info')
    avatar = models.ImageField(upload_to=AVATAR_DIR)

    def to_dict(self) -> Dict[str, Any]:
        return {
            JsonResponseDictConst.USER_NAME: self.user.username,
            JsonResponseDictConst.AVATAR: self.get_avatar_url(),
        }

    def get_entire_avatar_path(self) -> str:
        return settings.BASE_DIR / type(self).AVATAR_DIR / self.avatar.name

    def get_avatar_url(self) -> str:
        cls = type(self)

        return os.path.join(settings.STATIC_URL, settings.MEDIA_DIR, cls.AVATAR_DIR_NAME, self.avatar.name).replace('\\', '/')

    def change_avatar(self, img: Union[uploadedfile.InMemoryUploadedFile, None]) -> Union[None, 'UserInfo']:
        '''
        修改头像
        '''

        if not img:
            return None

        with open(self.get_entire_avatar_path(), 'wb') as old_avatar:
            for chunk in img.chunks():
                old_avatar.write(chunk)

        return self

    def delete(self, using = None, keep_parents = False) -> Tuple[int, Dict[str, int]]:
        os.remove(self.get_entire_avatar_path())
        return super().delete(using, keep_parents)

    @classmethod
    def create_for_user(cls, user: User) -> 'UserInfo':
        '''
        新建一个绑定到user的UserInfo

        头像采用默认头像
        '''

        avatar_name = f'{user.id}.png'
        new_avatar_path = os.path.join(settings.BASE_DIR, os.path.join(cls.AVATAR_DIR, avatar_name))
        shutil.copy(BackendConst.DEFAULT_USER_AVATAR, new_avatar_path)

        new_user_info = cls.objects.create(user=user, avatar=avatar_name)

        return new_user_info
