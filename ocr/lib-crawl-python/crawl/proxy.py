import re
import copy
import datetime
import os
import sys
sys.path.append(os.path.dirname(__file__))

from proxy_manager import ProxyManager

def _get_detail_attrs():
    default = [r for r in Detail.default_detail_attrs]
    return default

def is_int(val):
    try:
        val = int(val)
    except TypeError:
        return False
    return True

class Proxy(object):
    default_proxy_attrs = {'location':'Unknown', 'protocol':'http', 'id':None}
    required_proxy_attrs = ('address', 'port')

    def __init__(self, validate=True, **kwargs):
        self.proxy_mgr = ProxyManager()
        self.validate = validate
        try:
            self.address = kwargs['address']
            self.port = kwargs['port']
        except KeyError:
            raise Exception("Missing required attribute(s) address and/or port for Proxy object")

        for req in self.__class__.required_proxy_attrs:
            if not getattr(self, req):
                raise Exception("Attribute %s must evaluate to True" % req)

        for kwarg, default in self.__class__.default_proxy_attrs.items():
            if(kwarg in kwargs and kwargs[kwarg]):
                default = kwargs[kwarg]
            setattr(self, kwarg, default)

        if self.validate:
            self.do_proxy_validation()

        self.proxy_id = self.id
        print(self.proxy_id)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, addr):
        if not re.match(adr_re, addr):
            raise Exception("Invalid address only IPV4 supported.")
        else:
            self._address=addr

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        if is_int(port):
            self._port = port
        else:
            raise Exception("value %s is not an int" % port)

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        if protocol not in ('http','https','ssl','socksV4','socksV5','socks_v4','socks_v5','ftp'):
            raise Exception("Protocol must be http, https, ssl, socksv4, socksv5, or ftp")
        else:
            self._protocol = protocol

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if is_int(id) or id is None:
            self._id = id
            self._proxy_id = id
        else:
            raise Exception("Invalid ID, must be an integer")

    @property
    def proxy_id(self):
        return self._proxy_id

    @proxy_id.setter
    def proxy_id(self, pid):
        if pid is None:
            self._proxy_id = None
            return
        if is_int(pid):
            self._id=pid
            self._proxy_id = pid
            return


    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, loc):
        self._location = loc

    @property
    def last_active(self):
        return self._last_active

    @last_active.setter
    def last_active(self, la):
        if isinstance(la, datetime.datetime):
            self._last_active = la
        else:
            raise Exception("last_active time must be instance of datetime.datetime")


    def to_string(self):
        prefix = "http"
        if(re.compile("socks").search(self.protocol)):
            prefix = "socks"
        return "%s://%s:%s" % (prefix, self.address, self.port)

    @classmethod
    def from_string(self, str, **kwargs):
        regex = re.compile('^(http|socks)?(?:\:\/\/)?(.*):(.*)$')
        res = regex.findall(str)
        if(not res):
            raise Exception("Could not parse proxy string '%s'" %str)
        else:
            res = list(res[0])
            if not 'protocol' in kwargs:
                kwargs['protocol'] = res[0]
            return Proxy(address=res[1], port=res[2], **kwargs)

    def clone(self):
        return copy.copy(self)

    def do_proxy_validation(self):
        self.proxy_mgr.get_or_create_proxy_id(self)
