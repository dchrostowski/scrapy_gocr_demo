# scrapy web crawling demo with ocr

Just a very simple demo using scrapy coupled with gocr to read proxy server addresses from torvpn.com which are displayed in image files.  This uses my personal proxy api.  I'll leave it open for now but will immediately close access to the API if I see too many requests coming in.  "Too many" requests is a totally arbitrary number decided by me.

 ### Dependencies:
 * [gocr](http://jocr.sourceforge.net/)
 * virtualenv
 * see requirements.txt for python libraries
 

### Caution
Don't ruin it for everyone.  If you start heavily using my proxydump api, I will shut it down.  I'm sure that it's only a matter of time before a bot picks it up though.

### Usage
<b>
```
cd ocr/ocr/spiders
scrapy runspider torvpn_com.py
```
</b>

### Results
Downloaded images get saved to ocr/ocr/spiders/proxy_images/address.png
