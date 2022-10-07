import threading
import datetime
import time

from pytz import UTC

from .models import UserRoleRelation

# Create your views here.


class UserRoleRelationManager:
    '''
    用于定期删除过期UserRoleRelation的管理类，采用单例模式
    '''

    _INSTANCE_LOCK = threading.Lock()
    TIME_DELTA = datetime.timedelta(days=1)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_INSTANCE"):
            with cls._INSTANCE_LOCK:
                if not hasattr(UserRoleRelationManager, "_INSTANCE"):
                    cls._INSTANCE = object.__new__(cls)
        return cls._INSTANCE
        
    def clear_time_out_relations(self) -> None:
        while True:
            time.sleep(self.TIME_DELTA.total_seconds())
            
            time_out_tokens = UserRoleRelation.objects.filter(forever=False, 
                dead_time__lte=datetime.datetime.now(UTC))
            time_out_tokens.delete()

    def __init__(self):
        clear_thread = threading.Thread(target=self.clear_time_out_relations)
        clear_thread.setDaemon(True)
        clear_thread.start()

USER_ROLE_RELATION_MANAGER = UserRoleRelationManager()
