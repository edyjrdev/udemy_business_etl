import os
import json

class Auth:    
    def __init__(self):
        self.path_credential = 'auth'
        self.file_credential = 'credencial.json'
        self.file_path = os.path.join(self.path_credential, self.file_credential)
        self.credential = {}

    def start(self):
        try:
            with open(file=self.file_path, mode='r', encoding='utf-8') as file_json:
                data = json.load(file_json)
                cred = data[0]
                self.credential['clientid'] = cred['rest_client_id']
                self.credential['secretid']= cred['rest_client_secret']
                self.credential['account_name'] = cred['ACCOUNT_NAME']
                self.credential['account_id'] = cred['ACCOUNT_ID']
                return self.credential   
        except Exception as e:
            return {}
