# Created by SezerBozkir<admin@sezerbozkir.com> at 6/26/2020
"""
https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-References/agcapi-appid-list_v2
This is one of client for HMS Publishing API. Not all endpoints implemented.
For first step implemented critical ones. If you need to more, feel free to contact me.
"""
import requests
from http import HTTPStatus


class HmsPublishingApi:
    access_token = None
    upload_url = None
    chunk_upload_url = None
    auth_code = None
    app_id = None
    base_api = 'https://connect-api.cloud.huawei.com/api'
    publishing_api_link = 'https://www.huawei.com/auth/agc/publish'

    def __init__(self, client_id, client_secret, package_name, debug=False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.package_name = package_name
        self.debug = debug

        self.access_token = self.get_access_token()
        self.header = {
            'client_id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token,
        }
        self.app_id = self.get_app_id()
        self.params = {
            'appId': self.app_id,
        }

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
        if resp.status_code == HTTPStatus.OK:
            creds = resp.json()
            try:
                if self.debug:
                    print(f"Access Token: {creds['access_token']}\n valid: {creds['expires_in']}")
                self.access_token = creds['access_token']
            except:
                print(resp.json().get('ret').get('msg'))
        else:
            print(f"Error: {resp.status_code} {resp.reason}")
        return self.access_token

    def get_app_id(self):
        """
        How to get app id?
        https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-References/agcapi-appid-list_v2
        :return:
        """
        if self.app_id:
            return self.app_id

        params = {
            'client_id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token,
            'packageName': self.package_name
        }
        resp = requests.get(self.base_api + "/publish/v2/appid-list", headers=self.header, params=params)
        if resp.status_code == HTTPStatus.OK:
            if self.debug:
                print(f"App name: {resp.json()['appids'][0].get('key')}, App ID: {resp.json()['appids'][0].get('value')}")
            self.app_id = resp.json()['appids'][0].get('value')
        else:
            print(f"Error: {resp.status_code} {resp.reason}")
        return self.app_id

    def get_upload_url(self, file_type='apk'):
        if self.upload_url:
            return self.upload_url

        params = {
            'appId': self.app_id,
            'suffix': file_type
        }
        header = {
            'client_id': self.client_id,
            'Authorization': 'Bearer ' + self.access_token
        }
        resp = requests.get(self.base_api + "/publish/v2/upload-url", params=params, headers=header)
        if resp.status_code == HTTPStatus.OK:
            creds = resp.json()
            self.upload_url = creds['uploadUrl']
            self.chunk_upload_url = creds['chunkUploadUrl']
            self.auth_code = creds['authCode']
        return self.upload_url

    def upload_app(self, file_path, file_name, file_type):
        if not self.upload_url:
            self.upload_url = self.get_upload_url(file_type=file_type)

        header = {
            "accept": "application/json"
        }

        req_body = {
            'authCode': self.auth_code,
            'fileCount': 1
        }
        with open(file_path, 'rb') as f:
            first_phase = requests.post(self.upload_url,
                                        files={file_name: f},
                                        data=req_body,
                                        headers=header)
            if first_phase.status_code == HTTPStatus.OK:
                body = {
                    'fileType': 5,
                    'files': [{
                        'fileName': file_name,
                        'fileDestUrl': first_phase.json()['result']['UploadFileRsp']['fileInfoList'][0]['fileDestUlr'],
                        'size': str(first_phase.json()['result']['UploadFileRsp']['fileInfoList'][0]['size'])
                    }]
                }
                second_phase = requests.put(self.base_api + "/publish/v2/app-file-info",
                                            headers=self.header,
                                            json=body,
                                            params=self.params)

        return second_phase

    def get_app_info(self):
        """
        How to get App info?
        https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-References/agcapi-app-info_query_v2
        :return:
        """
        resp = requests.get(self.base_api + "/publish/v2/app-info", headers=self.header, params=self.params)
        return resp.json()

    def update_app_info(self, updated_details: dict):
        """
        How to update app information?
        https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-References/agcapi-app-info_update_v2

        :param updated_details: key value pairs you want to update
        :return:
        """
        body = dict()
        for key, value in updated_details.items():
            body[key] = value

        resp = requests.put(self.base_api + "/publish/v2/app-info", headers=self.header, data=body, params=self.params)
        if resp.status_code == HTTPStatus.OK:
            return resp.json()
        return resp

    def add_app_language(self, lang, app_name, app_desc=None, brief_info=None, new_features=None):
        """
        appName = App name in a language. This parameter is mandatory when a language type is added.
        appDesc = App description in a language.
        briefInfo = Brief description in a language.
        newFeatures = Introduction to the new version in a language.

        This API is used to update multi-language information about a specified app.
        If no multi-language information is available, this API is used to add the multi-language information.
        Callers of this API include account holders, administrators, app administrators, and operations personnel.
        https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-References/agcapi-app-language-info_update_v2
        :return:
        """
        body = {
            'lang': lang,
            'appName': app_name
        }

        if app_desc:
            body['appDesc'] = app_desc
        if brief_info:
            body['briefInfo'] = brief_info
        if new_features:
            body['newFeatures'] = new_features

        resp = requests.put(self.base_api + "/publish/v2/app-language-info",
                            headers=self.header,
                            data=body,
                            params=self.params)
        return resp

    def release_app(self):
        """
        https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-References/agcapi-app-submit_v2
        This API is used to submit a request for app approval. Before calling this API,
        ensure that the app information is complete and the app software package has been uploaded.
        Callers of this API include account holders, administrators, and app administrators.
        :return:
        """
        resp = requests.post(self.base_api + '/publish/v2/app-submit', headers= self.header, params=self.params)
        return resp
