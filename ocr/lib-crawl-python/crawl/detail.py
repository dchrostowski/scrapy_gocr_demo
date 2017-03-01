import os
import sys
sys.path.append(os.path.dirname(__file__))

from proxy import Proxy
import datetime

def is_int(val):
    try:
        val = int(val)
    except TypeError:
        return False
    return True

def _get_proxy_attrs():
    req = [r for r in Proxy.required_proxy_attrs]
    default = [d for d in Proxy.default_proxy_attrs.keys()]
    return default + req

class Detail(Proxy):
    default_detail_attrs = {'dirty':0,'active':0,'queue_id':1,'load_time_ms':0,
      'headless_load_time_ms':0,'last_active':datetime.datetime(1970,1,1),
      'last_used':datetime.datetime(1970,1,1)}

    def __init__(self, validate=True, **kwargs):
        print("\n\n\n\nINIT CALLED\n\n\n\n")
        #proxy_kwargs = merge_dicts(Proxy.default_proxy_attrs, proxy_kwargs)
        Proxy.__init__(self, validate=validate, **kwargs)
        self.validate = validate
        for kwarg, default in self.__class__.default_detail_attrs.items():
            if kwarg in kwargs:
                default = kwargs[kwarg]
            setattr(self, kwarg, default)
        if(self.validate):
            self.do_detail_validation()

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, flag):
        if is_int(flag) and flag == 0 or flag == 1:
            self._dirty=flag
        else:
            raise Exception("Flag must be an int with value 0 or 1")

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        if is_int(active) and active == 1 or active == 0:
            self._active=active
        else:
            raise Exception("active flag must be 1 or 0")

    @property
    def queue_id(self):
        return self._queue_id

    @queue_id.setter
    def queue_id(self, qid):
        if is_int(qid):
            self._queue_id = qid
        else:
            raise Exception("invalid queue id")

    @property
    def load_time_ms(self):
        return self._load_time_ms

    @load_time_ms.setter
    def load_time_ms(self, ms):
        if is_int(ms):
            self._load_time_ms = ms
        else:
            raise Exception("load time must be an int")

    @property
    def headless_load_time_ms(self):
        return self._headless_load_time_ms

    @headless_load_time_ms.setter
    def headless_load_time_ms(self, ms):
        if is_int(ms):
            self._headlesss_load_time_ms = ms
        else:
            raise Exception("load time must be an int")

    @property
    def proxy_id(self):
        return self._id

    @proxy_id.setter
    def proxy_id(self, pid):
        if is_int(pid) or pid is None:
            self._id=pid
            self._proxy_id=pid
        else:
            raise Exception("proxy id must be int or None")

    def time_getter(self, field_name):
        return getattr(self,'_%s' % field_name)

    def time_setter(self, field_name, field_val):
        if isinstance(field_val, datetime.datetime):
            setattr(self, '_%s'%field_name, field_val)
        else:
            raise Exception("%s be a datetime instance" % field_name)

    @property
    def last_active(self):
        return self.time_getter('last_active')

    @last_active.setter
    def last_active(self, la):
        return self.time_setter('last_active',la)

    @property
    def last_used(self):
        return self.time_getter('last_used')

    @last_used.setter
    def last_used(self, lu):
        return self.time_setter('last_used', lu)

    @classmethod
    def from_proxy_id(self, proxy_id):
        # TODO
        pass

    @classmethod
    def from_detail_id(self, detail_id):
        # TODO
        pass

    @classmethod
    def new_from_proxy(self, proxy, validate=True, **detail_kwargs):
        # TODO
        pass

    def create_or_get_detail_id(self):
        # TODO
        pass

    def do_detail_validation(self):
        print ("VALIDATING DETAIL")
        pass
