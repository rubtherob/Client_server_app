import sys
import logging
import config_log_server
import config_log_client
import traceback
import inspect

if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')



def log_decorator(func):
    def decorated(*args, **kwargs):
        ret = func(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func.__name__} из функции {inspect.stack()[1][3]}')
        return ret
    return decorated
