import os
import json
import mysql.connector
from mysql.connector import errorcode

class Config(dict):
    def __init__(self):
        self._config_file = os.path.dirname(os.path.realpath(__file__)) + \
        '/config.json'
        try:
            with open(self._config_file) as config:
                self.update(json.load(config))
        except FileNotFoundError as fe:
            print("Problem finding %s: %s" % (self._config_file, fe))
        except ValueError as ve:
            print("Problem parsing file %s: %s" % (self._config_file, ve))
        if len(self) < 1:
            raise Exception("Invalid configuration")
    
    @property
    def proxy_db(self):
        db_params = self['proxy_database']
        try:
            dbh = mysql.connector.connect(**db_params)
        except mysql.connector.Error as err:
            print(err)
            return None
        else:
            return dbh
    @property        
    def crawl_db(self):
        db_params = self['crawl_database']
        try:
            dbh = mysql.connector.connect(**db_params)
        except mysql.connector.Error as err:
            print(err)
            return None
        else:
            return dbh
