import re
import requests
import ssl

from os.path import join
from requests.exceptions import ConnectionError


from constants.constants import CERT_FILE_EXTENSION, RESOURCES_CERTS_FOLDER_PATH
from config.config_provider import config
from utils.file_utils import read_file


def test_is_available():
    try:
        response = requests.get(config.test_resource_url, verify=False)
        response.close()
        assert response.status_code == 200, (f'Ресурс "{config.test_resource_url}" '
                                             f'вернул код ответа {response.status_code}')
        response_html = response.text
        if re.match('^.*<head>.*<title>[^\\<\\>]*<\\/title>.*<\\/head>.*$', response_html):
            response_header = response_html.split('<title>', 2)[-1].split('</title>', 2)[0]
        else:
            response_header = None
        assert response_header == config.test_resource_main_page_header, \
            (f'Заголовок страницы равный "{response_header}" не соответствует '
             f'ожидаемому значению "{config.test_resource_main_page_header}"')
    except ConnectionError:
        assert False, f'Ресурс "{config.test_resource_url}" недоступен'


def test_is_secure():
    cert_path = join(RESOURCES_CERTS_FOLDER_PATH, f'{config.test_resource_public_cert_name}.{CERT_FILE_EXTENSION}')
    expected_cert = read_file(cert_path)
    clean_resource_url = re.sub('\\/$', '', re.sub('^.*\\/\\/', '', config.test_resource_url))

    try:
        actual_cert = ssl.get_server_certificate((clean_resource_url, 443))
    except Exception as e:
        assert False, f'Не получается получить сертификат тестового ресурса в свзи с ошибкой:\n{e}'

    assert actual_cert == expected_cert, ('Сертификат сервера недействителен.\n'
                                          f'Ожидается\n{expected_cert}\n'
                                          f'Получено:\n{actual_cert}')
