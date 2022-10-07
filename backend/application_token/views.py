import threading
import datetime
import time

from pytz import UTC

from .models import ApplicationToken

# Create your views here.


class TokenManager:
    '''
    用于定期删除过期ApplicationToken的管理类，采用单例模式
    '''

    _INSTANCE_LOCK = threading.Lock()
    TIME_DELTA = datetime.timedelta(days=1)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_INSTANCE"):
            with cls._INSTANCE_LOCK:
                if not hasattr(TokenManager, "_INSTANCE"):
                    cls._INSTANCE = object.__new__(cls)
        return cls._INSTANCE
        
    def clear_time_out_tokens(self) -> None:
        while True:
            time.sleep(self.TIME_DELTA.total_seconds())
            
            time_out_tokens = ApplicationToken.objects.filter(forever=False, 
                dead_time__lte=datetime.datetime.now(UTC))
            time_out_tokens.delete()

    def __init__(self):
        clear_thread = threading.Thread(target=self.clear_time_out_tokens)
        clear_thread.setDaemon(True)
        clear_thread.start()

TOKEN_MANAGER = TokenManager()
