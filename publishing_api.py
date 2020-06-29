# Created by SezerBozkir<admin@sezerbozkir.com> at 6/26/2020
import requests
from http import HTTPStatus
from pub_env import *


class HmsPublishingApi:
    access_token = None
    upload_url = None
    chunk_upload_url = None
    auth_code = None
    app_id = None
    base_api = 'https://connect-api.cloud.huawei.com/api'
    publishing_api_link = 'https://www.huawei.com/auth/agc/publish'

    def __init__(self, client_id, client_secret, package_name):
        self.client_id = client_id
        self.client_secret = client_secret
        self.package_name = package_name

        self.access_token = self.get_access_token()
        self.app_id = self.get_app_id()

    def get_access_token(self):
        """
        How to get access token?
        https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-References/obtain_token
        :return:
        """
        if self.access_token:
            return self.access_token

        api_credentials = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        resp = requests.post(self.base_api + "/oauth2/v1/token", json=api_credentials)
        access_token = None
        if resp.status_code == HTTPStatus.OK:
            creds = resp.json()
            print(f"Access Token: {creds['access_token']}\n valid: {creds['expires_in']}")
            access_token = creds['access_token']
        else:
            print(f"Error: {resp.status_code} {resp.reason}")
        return access_token

    def get_app_id(self):
        """
        How to get app id?
        https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-References/agcapi-appid-list_v2
        :return:
        """
        if not self.access_token:
            self.access_token = self.get_access_token()

        if self.app_id:
            return self.app_id

        header = {
            'client_id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token,
        }

        params = {
            'client_id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token,
            'packageName': self.package_name
        }
        resp = requests.get(self.base_api + "/publish/v2/appid-list", headers=header, params=params)
        if resp.status_code == HTTPStatus.OK:
            print(f"App name: {resp.json()['appids'][0].get('key')}, App ID: {resp.json()['appids'][0].get('value')}")
            self.app_id = resp.json()['appids'][0].get('value')
        else:
            print(f"Error: {resp.status_code} {resp.reason}")
        return self.app_id

    def get_upload_url(self, upload_file_type='apk'):
        if not self.access_token:
            self.access_token = self.get_access_token()

        if not self.app_id:
            self.app_id = self.get_app_id()

        if self.upload_url:
            return self.upload_url

        params = {
            'appId': self.app_id,
            'suffix': upload_file_type
        }
        header = {
            'client_id': client_id,
            'Authorization': 'Bearer ' + self.access_token
        }
        resp = requests.get(self.base_api + "/publish/v2/upload-url", params=params, headers=header)
        if resp.status_code == HTTPStatus.OK:
            creds = resp.json()
            self.upload_url = creds['uploadUrl']
            self.chunk_upload_url = creds['chunkUploadUrl']
            self.auth_code = creds['authCode']
        return self.upload_url

    def upload_app(self, file_name):
        if not self.access_token:
            self.access_token = self.get_access_token()
        if not self.app_id:
            self.app_id = self.get_app_id()
        if not self.upload_url:
            self.upload_url = self.get_upload_url()

        header = {
            'client_id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token,
            "Content-Type": "application/json"
        }

        req_body = {
            'authCode': self.auth_code,
            'fileCount': 1,
            'name': file_name
        }
        #  + "/publish/v2/app-package-file"
        with open('sample-apk.apk', 'rb') as f:
            resp = requests.post(self.upload_url,
                                 files={'file': f},
                                 data=req_body,
                                 params={'appid': self.app_id},
                                 headers=header)
        return resp

    def get_app_info(self):
        """
        How to get App info?
        https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-References/agcapi-app-info_query_v2
        :return:
        """
        if not self.access_token:
            self.access_token = self.get_access_token()

        if not self.app_id:
            self.app_id = self.get_app_id()

        header = {
            'client_id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token,
        }

        params = {
            'appId': self.app_id,
        }
        resp = requests.get(self.base_api + "/publish/v2/app-info", headers=header, params=params)
        return resp.json()


if __name__ == '__main__':
    my_hms_api = HmsPublishingApi(client_id, client_secret, package_name)
    # respii = my_hms_api.upload_app('sample-apk.apk')
    # pprint(respii)
    my_hms_api.get_app_id()
