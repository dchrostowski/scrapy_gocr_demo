# -*- coding: utf-8 -*-


# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
#dir_path = "%s/lib_crawl_python" % dir_path
sys.path.append(dir_path)

import urllib
import calendar
import json
import time
import re
import scrapy
import random
print(sys.path)
from lib_crawl_python.crawl.proxy import Proxy

PROXY_LIST_FILE = '../proxies.list'


class GlSpidersSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyFetcher(object):
    def __init__(self):
        if os.path.exists(PROXY_LIST_FILE):
            if self.proxy_sync_time() > 30*60:
                self.make_proxy_file()
        else:
            self.make_proxy_file()

    def proxy_sync_time(self):
        mtime = os.path.getmtime(PROXY_LIST_FILE)
        currtime = calendar.timegm(time.gmtime())
        diff = currtime - mtime
        return diff


    def make_proxy_file(self):
        
        proxy_dump_url = 'https://proxydump.streetscrape.com/?password=Qu1x3Y!&limit=200&location=united+states'
        content = urllib.request.urlopen(proxy_dump_url).read().decode('utf-8')
        json_proxies = json.loads(content)
        ofh = open(PROXY_LIST_FILE, 'w')

        for proxy in json_proxies:
            proxy = Proxy(validate=False,address=proxy['address'],
              port=proxy['port'], protocol=proxy['protocol']
            )
            socks_re = r'^socks.+'
            if not re.match(socks_re, proxy.protocol):
                ofh.write("%s\n" % proxy.to_string())

        ofh.close()


class GLProxyMiddleware(object):
    def __init__(self, *args, **kwargs):
        fetcher = ProxyFetcher()
        self.proxy_pool = self.get_proxy_pool()

    def renew_proxy_pool(self):
        fetcher = ProxyFetcher()
        fetcher.make_proxy_file()
        self.proxy_pool = self.get_proxy_pool()


    def get_proxy_pool(self):
        ifh = open(PROXY_LIST_FILE, 'r')
        proxies = []

        line = ifh.readline()
        while line:
            proxies.append(line)
            line=ifh.readline()
        ifh.close()

        return proxies

    def process_request(self, request, spider):
        print("getting %s " % request.url)
        if ProxyFetcher().proxy_sync_time() > 30*60:
            self.renew_proxy_pool()
        
        request.meta['proxy'] = random.choice(self.proxy_pool)
        print("process request: using proxy %s" % request.meta['proxy'])


    def process_response(self, request, response, spider):
        redirects=[]
        if 'redirect_urls' in request.meta:
            redirects = request.meta['redirect_urls']
        for redir in redirects:
            print(redir)
        if response.status != 404 and response.status != 200:
            request.meta['proxy'] = random.choice(self.proxy_pool)
            
            return request
        return response

    def process_exception(self, request, exception, spider):
        print("exception occurred")
        redirects=[]
        if 'redirect_urls' in request.meta:
            redirects = request.meta['redirect_urls']
        for redir in redirects:
            print(redir)
        request.meta['proxy'] = random.choice(self.proxy_pool)
        print("process_exception: using proxy %s" % request.meta['proxy'])
        return request
