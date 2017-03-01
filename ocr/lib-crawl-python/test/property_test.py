#!/usr/bin/env python

import datetime

class PropertyTest(object):
    default_detail_attrs = {'dirty':0,'active':0,'queue_id':1,'load_time_ms':0,
      'headless_load_time_ms':0,'last_active':datetime.date(1970,1,1),
      'last_used':datetime.date(1970,1,1)}
    def __init__(self, *args, **kwargs):
        for key, val in self.__class__.default_detail_attrs.items():
            if key in kwargs:
                val = kwargs[key]
            setattr(self, key, val)
