import sqlite3
import sys
import time 

class AF_DB:
    def __init__(self):
        self.open_db()

    def open_db(self):
        self.connection = sqlite3.connect("py_af.db")
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()

    def get_settings(self):
        """ Returns a dictionary of all settings. """
        try:
            self.cursor.execute('SELECT * FROM settings')
            settings = self.cursor.fetchall()[0]
            settings = {"ga_api_key" : settings[0],
                        "ga_url" : settings[1],
                        "oauth_scope" : settings[2],
                        "oauth_endpoint" : settings[3],
                        "oauth_token_url" : settings[4],
                        "oauth_redirect_uri" : settings[5],
                        "oauth_client_id" : settings[6],
                        "oauth_client_secret" : settings[7],
                        "oauth_refresh_token" : settings[8],
                        "oauth_access_token" : settings[9]
                        }
            return settings
        except(sqlite3.Error, e):
            print("Error %s:" % e.args[0])
            sys.exit(1)
        finally:
            if self.cursor:
                self.close()

    def add_settings(self, ga_api_key, ga_url, oauth_scope, oauth_endpoint,
                    oauth_token_url, oauth_redirect_uri, oauth_client_id,
                    oauth_client_secret, oauth_refresh_token=None,
                    oauth_access_token=None):
        self.cursor.execute('INSERT INTO settings VALUES(?,?,?,?,?,?,?,?,?,?)',
                           (ga_api_key, ga_url, oauth_scope, oauth_endpoint,
                            oauth_token_url, oauth_redirect_uri,
                            oauth_client_id, oauth_client_secret,
                            oauth_refresh_token, oauth_access_token))
        self.connection.commit()
        self.close()

    def update_access_token(self, oauth_access_token): 
        try:
            self.open_db()
            self.cursor.execute('UPDATE settings SET oauth_access_token=?',
                           (oauth_access_token,))
            self.connection.commit()
        except(sqlite3.Error, e):
            print("Update error: ?", (e.args[0],))
            sys.exit(1)
        finally:
            self.close()