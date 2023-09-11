import re


from constants.constants import HTTPS_PROTOCOL_STR
from utils.json_utils import read


class Config:

    def __init__(self, config_json_path):
        self.config = read(config_json_path)

    @property
    def test_resource_url(self):
        value = str(self.config['test_resource']['https_url'])
        if value.startswith('https://'):
            return value
        value = re.sub('^[A-Z]|[a-z]|[0-9]*\\/\\/.*$', '', value)
        return HTTPS_PROTOCOL_STR + value

    @property
    def test_resource_main_page_header(self):
        return self.config['test_resource']['main_page_header']

    @property
    def test_resource_public_cert_name(self):
        return self.config['test_resource']['cert_name']
