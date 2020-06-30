# Created by SezerBozkir<admin@sezerbozkir.com> at 6/30/2020
from publishing_api import HmsPublishingApi
from pub_env import client_id, client_secret, package_name

if __name__ == '__main__':
    my_api = HmsPublishingApi(client_id, client_secret, package_name)
    my_api.release_app()