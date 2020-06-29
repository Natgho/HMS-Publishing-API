# Created by SezerBozkir<admin@sezerbozkir.com> at 6/29/2020
from publishing_api import HmsPublishingApi
from pub_env import client_id, client_secret, package_name

if __name__ == '__main__':
    my_api = HmsPublishingApi(client_id, client_secret, package_name)
    app_id = my_api.get_app_id()
