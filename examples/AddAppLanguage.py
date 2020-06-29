# Created by SezerBozkir<admin@sezerbozkir.com> at 6/29/2020
from publishing_api import HmsPublishingApi
from pub_env import client_id, client_secret, package_name
from pprint import pprint

if __name__ == '__main__':
    my_api = HmsPublishingApi(client_id, client_secret, package_name)
    app_info = my_api.add_app_language(lang='zh-CN',
                                       app_name='PushSunucuOrnegi',
                                       app_desc='Bu bir API ustunden Push sunucu ornegidir')

    pprint(app_info)
