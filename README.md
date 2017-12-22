# 使用scrapy 批量采集MM图片
某天看到了一个MM图片的网站，就分别使用了requsts+Bs4和scrapy下载了。果然scrapy要快的多。
## 分析网站
[MM网站](http://www.5442.com/special/)这个网站的结构挺简单的，也没有什么反爬虫的手段。难点就是这个保存路径的问题，别的难度都不大。<br/>
* 先解析首页，然后获取每个频道页的名称和地址。<br/>
```
import scrapy
from mm.items import  MmItem
from scrapy.http import Request

class MmzhaopianSpider(scrapy.Spider):
    name = 'mmzhaopian'
    allowed_domains = ['www.5442.com']
    start_urls = ['http://www.5442.com/special']

    def parse(self, response):
        pindaourls = response.xpath('//div[@class="contc"]/a/@href').extract()
        pindaonames = response.xpath('//div[@class="contc"]/span/a/text()').extract()
        for i in range(len(pindaourls)):
            pindaourl = pindaourls[i]
            pindaoname = pindaonames[i]
            yield Request(pindaourl,callback=self.get_gerenurl,meta={'name':pindaoname})
```
* 然后解析频道页，获取每个主题的名称和地址。<br/>
```
    def get_gerenurl(self,response):
        gerenurls = response.xpath('//div[@class="title"]/span/a/@href').extract()
        gerenmames = response.xpath('//div[@class="title"]/span/a/text()').extract()
        for i in range(len(gerenurls)):
            gerenurl = gerenurls[i]
            gerenmame = response.meta['name'] +'/'+ gerenmames[i]
            yield Request(gerenurl,callback=self.get_mmurl,meta={'name':gerenmame})
```
* 由于主题是多页结构，先解析第一页，获取总页码，然后生成每一页的地址。<br/>
```
def get_mmurl(self,response):
        base_url = response.url[:-5]
        yema = response.xpath('//div[@class="page"]/ul/li[1]/a/text()').re(r'共(.*?)页')[0]
        for i in range(1,int(yema)+1):
            mmurl = base_url + '_' + str(i) +'.html'
            mmname = response.meta['name']
            yield Request(mmurl,callback=self.get_info,meta={'name': mmname})
```
* 抓取每一页的图片并储存。<br/>
```
    def get_info(self,response):
        item = MmItem()
        urls = response.xpath('//p[@align="center"]/a/img/@src').extract()
        for i in range(len(urls)):
            url = urls[i]
            name = response.meta['name'] +'/'+ url.split('/')[-1]
            item['images_url'] = [url]
            item['images_path']= name[:-8]
            yield item
```
