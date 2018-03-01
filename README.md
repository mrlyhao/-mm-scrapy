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

# python文件合集

### * 使用scrapy 批量采集MM图片 [点击查看](https://github.com/mrlyhao/mmscrapy)
### * 使用scrapy爬取拉勾网职位信息，并异步保存在mysql中[点击查看](https://github.com/mrlyhao/bole/tree/master/bole)
### * 使用scrapy-redis爬取拉勾，Windows为slave，linux为master。[点击下载](https://github.com/mrlyhao/lagou_redis)

### * 使用beautifulsoup 批量抓取MM照片，[点击查看](https://github.com/mrlyhao/lianxi/blob/master/mm%E7%85%A7%E7%89%87%E6%89%B9%E9%87%8F%E7%88%AC%E5%8F%96.py)
### * 采集后台数据，分析每本书的情况 [点击查看](https://github.com/mrlyhao/lianxi/blob/master/%E4%B9%A6%E4%B8%9B%E5%90%8E%E5%8F%B0%E6%95%B0%E6%8D%AE%E9%87%87%E9%9B%86.py)
### * 采集京东数据并保存在表格中 [点击查看](https://github.com/mrlyhao/lianxi/blob/master/%E4%BA%AC%E4%B8%9C%E7%88%AC%E8%99%AB.py)和[pandas版本](https://github.com/mrlyhao/lianxi/blob/master/%E4%BA%AC%E4%B8%9C%E7%88%AC%E8%99%ABpandas.py)
### * 简单爬取淘宝数据 [点击查看](https://github.com/mrlyhao/lianxi/blob/master/%E6%B7%98%E5%AE%9D%E5%95%86%E5%93%81%E4%BF%A1%E6%81%AF%E5%AE%9A%E5%90%91%E7%88%AC%E8%99%AB.py)
### * 爬取网上ip验证后储存 [点击查看](https://github.com/mrlyhao/lianxi/blob/master/%E5%A4%9AIP%E4%BB%A3%E7%90%86.py)
### * 爬取妹子图，解决图片重定向问题 [点击查看](https://github.com/mrlyhao/lianxi/blob/master/%E5%A6%B9%E5%AD%90%E5%9B%BE.py)
### * 有道翻译输入查询词，并爬取结果 [点击查看](https://github.com/mrlyhao/lianxi/blob/master/%E6%9C%89%E9%81%93%E7%BF%BB%E8%AF%91%E6%8F%90%E4%BA%A4.py)
### * 简单爬取今日头条 [点击查看](https://github.com/mrlyhao/lianxi/blob/master/%E7%88%AC%E5%8F%96%E4%BB%8A%E6%97%A5%E5%A4%B4%E6%9D%A1.py)和今日头条美女图 [点击查看](https://github.com/mrlyhao/lianxi/blob/master/%E7%88%AC%E5%8F%96%E4%BB%8A%E6%97%A5%E5%A4%B4%E6%9D%A1%E7%BE%8E%E5%A5%B3%E5%9B%BE.py)
### * 使用selenium爬取空间说说 [点击查看](https://github.com/mrlyhao/lianxi/blob/master/%E7%88%AC%E5%8F%96%E5%A5%BD%E5%8F%8B%E7%A9%BA%E9%97%B4%E8%AF%B4%E8%AF%B4.py)
### * 爬取微博热搜榜，清除干扰代码后，转换成中文 [点击查看](https://github.com/mrlyhao/lianxi/blob/master/%E7%88%AC%E5%8F%96%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C%E6%A6%9C.py)
