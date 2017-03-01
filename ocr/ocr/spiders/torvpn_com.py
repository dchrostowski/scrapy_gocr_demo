# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.contrib.pipeline.files import FilesPipeline
import re
import os
from subprocess import call


class TorvpnComSpider(scrapy.Spider):
    name = "torvpn.com"
    allowed_domains = ["www.torvpn.com"]
    start_urls = ['https://www.torvpn.com/en/proxy-list']
    
    def get_media_requests(self, item, info):
        for url in item['file_urls']:
            yield scrapy.Request(url=url)

    def parse(self, response):
        image_urls = response.xpath('.//table//tr/td[2]/img[contains(@alt, "IP")]/@src').extract()
        image_urls = [response.urljoin(url) for url in image_urls]
        for url in image_urls:
            yield Request(url=url, callback=self.process_images)

    def process_images(self, resp):
        file_re = r'\/([^\/]+)$'
        cwd = os.path.dirname(os.path.realpath(__file__))
        img_dir = cwd + '/proxy_images/'
        str_res = re.search(file_re, resp.url)
        filename = img_dir + str_res.group(1)
        print ("writing %s" % filename)
        with open(filename, 'wb') as fh:
            fh.write(resp.body)
        ret = os.popen("gocr -a 20 -i " + filename).read().rstrip()
        # All 7s get red as underscores.  Since we're only dealing with digits 0-9 in IPv4 IP addresses and 7 is the only missing we can safely
        # make the assumption that anything that is an underscore should be a 7.
        ret = re.sub(r'_', '7', ret)
        print("got address %s" % ret)
        
        #ip_re = r'(.)$'
        #ret = re.sub(r'(.)$', '', ret)
        newfile= "%s%s.png" % (img_dir,ret)
        call(["mv",filename,newfile])
            
        
        
