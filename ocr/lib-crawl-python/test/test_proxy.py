from pprint import pprint
import sys
import os
curr_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(curr_dir,'crawl')))
from proxy import Proxy
from config import Config

proxy = Proxy(address="1.1.1.1", port=3128, protocol="socksV5")

print(proxy.to_string())


print(dir(proxy))

attrs = ('id', 'port', 'address', 'location','protocol')

for attr in attrs:
    print (getattr(proxy, attr))

config = Config()
print("config's dirname is " + config._config_file)
pprint(config.config['proxy_database'])

dbh = config.proxy_db()
if dbh is not None:
    cursor = dbh.cursor()
    try:
        cursor.execute("SELECT * FROM details ORDER BY last_used ASC LIMIT 10")
    except mysql.connector.Error as err:
        print(err)
        exit(1)
