import requests
from bs4 import BeautifulSoup
import json

import af_db

class GA:
    def __init__(self):
        self.db = af_db.AF_DB()
        self.settings = self.db.get_settings()
        if self.settings["oauth_access_token"] is None:
            self.refresh_token()
        else:
          self.oauth_access_token = self.settings["oauth_access_token"]

    def generate_request(self):
        """
        Generate URL for client-side authorisation of account access
        """
        return "%sclient_id=%s&scope=%s&redirect_uri=%s&response_type=code" % \
                (self.settings["oauth_endpoint"], self.settings["oauth_client_id"], \
                self.settings["oauth_scope"], self.settings["oauth_redirect_uri"])

    def get_tokens(self, auth_token):
        """
        Use received auth code for generation of refresh + access codes.
        """
        payload = {'code':auth_token,
                  'client_id': self.settings["oauth_client_id"],
                  'client_secret':self.settings["oauth_client_secret"],
                  'redirect_uri':self.settings["oauth_redirect_uri"],
                  'grant_type':'authorization_code'}
        connection = requests.post(self.settings["oauth_token_url"], data=payload)
        return connection.content

    def refresh_token(self):
        """
        Use refresh token to generate new access_token
        """
        payload = {'client_id':self.settings["oauth_client_id"],
                  'client_secret':self.settings["oauth_client_secret"],
                  'refresh_token':self.settings["oauth_refresh_token"],
                  'grant_type':'refresh_token'}
        connection = requests.post(self.settings["oauth_token_url"], data=payload)
        response = json.loads(connection.content.decode("utf-8"))
        if "access_token" in response :
            self.oauth_access_token = response["access_token"]
            print("New refreshed access token: %s" % self.oauth_access_token)
            self.db.update_access_token(self.oauth_access_token)
            return connection.content
        else:
            return "Something went wrong:" + connection.content.decode("utf-8")

    def gen_url(self, **kwargs):
        url = self.settings["ga_url"]+'ids=ga:'+kwargs['ga_id']+\
            '&start-date='+ kwargs['start_date']+\
            '&end-date='+ kwargs['end_date']+\
            '&dimensions='+kwargs['dimensions']

        if kwargs['filters']:
            url += '&filters='+kwargs['filters']

        if kwargs['segment']:
            url += '&segment='+kwargs['segment']

        url += '&metrics='+kwargs['metrics']+'&sort='+kwargs['sort']+\
                '&max-results='+kwargs['max_results'] + "&key=" + self.settings["ga_api_key"]

        return url

    def pull_ga_data(self, url):
        """
        Carry out data pull
        TODO: include recursive nextLink check. 

        """
        header = {'Authorization':'OAuth '+ self.oauth_access_token}
        connection = requests.get(url, headers=header)
        if connection.status_code == 401:
            self.refresh_token()
            print("Old access token, refreshed with token: ", self.oauth_access_token)
            header = {'Authorization':'OAuth '+ self.oauth_access_token}
            connection = requests.get(url,headers=header)
        output = json.loads(connection.content.decode("utf-8"))
        return output

    def get_data(self, **kwargs):
        url = self.gen_url(**kwargs)
        data = self.pull_ga_data(url)

        if 'error' in data:
            print("Error: ", data['error']['code'], data['error']['message'])
        elif not 'rows' in data:
            print("No results found")
            print(data)
        else:
            return data

