#!/usr/bin/env python
import sys
import os.path
curr_dir = os.path.dirname(__file__)
print(curr_dir)
sys.path.append(os.path.abspath(os.path.join(curr_dir,'crawl')))
#par_dir = os.path.join(curr_dir, os.pardir)
#abs_par_dir = os.path.abspath(par_dir)
#sys.path.append(abs_par_dir)


print(sys.path)
from detail import Detail

proxy_args = {'address':'1.1.1.1', 'port':2323}
d = Detail(proxy_args)

print(d.address)
print(d.protocol)
