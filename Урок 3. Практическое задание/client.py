import config_log_client
import logging
import sys
import json
import socket
import time
from errors import ReqFieldMissingError
import argparse
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
from decorator import log_decorator


CLIENT_LOGGER = logging.getLogger('client')

@log_decorator
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформированно {PRESENCE} сообщение для {account_name}')
    return out

@log_decorator
def process_ans(message):
    CLIENT_LOGGER.debug('Разбор сообщения')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError

@log_decorator
def create_parser_comstr():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_ad', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser

def main():

    parser = create_parser_comstr()
    ip_with_port = parser.parse_args(sys.argv[1:])
    server_port = ip_with_port.port
    server_address = ip_with_port.ip_ad
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)
    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                    f'адрес сервера: {server_address}, порт: {server_port}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')

if __name__ == '__main__':
    main()
