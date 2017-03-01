import sys
import os
curr_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(curr_dir,'crawl')))
from proxy import Proxy
from config import Config
from pprint import pprint

proxy = Proxy(address="1.1.1.1", port=3128, protocol="ssl")
print("protocol is %s" % proxy.protocol)
print("address is %s" % proxy.address)
print("port is %s" % proxy.port)

print(proxy.to_string())

new_proxy = Proxy.from_string("1.1.1.1:4949", location="usa", protocol="socksV5")
print(new_proxy)

print("address: %s" % new_proxy.address)
print("protocol: %s" % new_proxy.protocol)
print("port: %s" % new_proxy.port)
print("location: %s" % new_proxy.location)
print(new_proxy.to_string())

cloned_proxy = new_proxy.clone()
print("cloned address: %s" % cloned_proxy.address)
print("cloned protocol: %s" % cloned_proxy.protocol)
print("cloned port: %s" % cloned_proxy.port)
print("cloned location: %s" % cloned_proxy.location)
print(cloned_proxy.to_string())

#print(Proxy.required_attrs)
#print(Proxy.default_attrs)

#print(Proxy.default_attrs.keys())

attrs1 = [a for a in Proxy.default_proxy_attrs.keys()].extend([1])
print(attrs1)

#bad_proxy = Proxy.from_string("asdaf;asdf", location="usa")
#print(bad_proxy)
