# Created by SezerBozkir<admin@sezerbozkir.com> at 6/29/2020
from publishing_api import HmsPublishingApi
from pub_env import client_id, client_secret, package_name

if __name__ == '__main__':
    my_api = HmsPublishingApi(client_id, client_secret, package_name)
    before_app_info = my_api.get_app_info()
    print("Before language: " +  before_app_info['appInfo']['defaultLang'])
    # default lang is sample. if you want to look at all of parameters, you can look at:
    # https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-References/agcapi-app-info_update_v2
    update_vals = {'defaultLang': 'en-US'}
    my_api.update_app_info(update_vals)
    after_app_info = my_api.get_app_info()
    print("After Language: " + after_app_info['appInfo']['defaultLang'])
