# Created by SezerBozkir<admin@sezerbozkir.com> at 6/29/2020
# Created by SezerBozkir<admin@sezerbozkir.com> at 6/29/2020
from publishing_api import HmsPublishingApi
from pub_env import client_id, client_secret, package_name
from pprint import pprint

if __name__ == '__main__':
    my_api = HmsPublishingApi(client_id, client_secret, package_name)
    full_path = r"C:\Users\SezerBozkir\PycharmProjects\sample_path\sample_apk_file.apk"
    file_name = 'sample_apk_file.apk'
    file_type = 'apk'  # apk or aab
    app_info = my_api.upload_app(file_path=full_path,
                                 file_name=file_name,
                                 file_type=file_type)
