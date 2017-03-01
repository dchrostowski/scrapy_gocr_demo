from config import Config
import mysql.connector
from mysql.connector import errorcode

conf = Config()

def mysql_err(err):
    print(err)
    exit(1)

class ProxyManager(object):
    print("\n\n\n\nINIT CALLED\n\n\n\n")

    def __init__(self, proxy_dbh=None, cache=None):
        self.config = Config()
        self.dbh = None
        if self.config['init_db_connection']:
            self.dbh=config.db


    @classmethod
    def get_or_create_proxy_id(self, proxy, update_proxy=True):
        cursor = Config.dbh.cursor()
        query = 'SELECT id, port, location, protocol FROM proxies WHERE address = %s';
        print(type(proxy.address))
        try:
            cursor.execute(query, (proxy.address,))
        except mysql.connector.Error as err:
            print("exception at first try/catch")
            mysql_err(err)

        rows = cursor.fetchall()
        print("cursor.rowcount is %s" % cursor.rowcount)

        if rows:
            proxy.id = rows[0][0]
            proxy.proxy_id = rows[0][0]
            db_port = rows[0][1]
            db_location = rows[0][2]
            db_protocol = rows[0][3]

            if(update_proxy and db_port == proxy.port and db_location == proxy.location and db_protocol == proxy.protocol):
                upate_proxy = False

            if update_proxy:
                query = 'UPDATE proxies set protocol=%s, port=%s, location=%s WHERE id=%s'
                cursor.execute(query, (proxy.protocol, proxy.port, proxy.location, proxy.id))
                ProxyManager.dbh.commit()
        else:
            query = """INSERT INTO proxies (protocol, address, port, location) VALUES ("%s","%s","%s","%s")"""
            try:
                cursor.execute(query, (proxy.protocol, proxy.address, proxy.port, proxy.location))
                ProxyManager.dbh.commit()
            except mysql.connector.Error as err:
                mysql_err(err)
            finally:
                proxy.id = cursor.lastrowid
                proxy.proxy_id = cursor.lastrowid
                ProxyManager.dbh.close()
