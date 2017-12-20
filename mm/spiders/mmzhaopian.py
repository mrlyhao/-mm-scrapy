# -*- coding: utf-8 -*-
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

    def get_gerenurl(self,response):
        gerenurls = response.xpath('//div[@class="title"]/span/a/@href').extract()
        gerenmames = response.xpath('//div[@class="title"]/span/a/text()').extract()
        for i in range(len(gerenurls)):
            gerenurl = gerenurls[i]
            gerenmame = response.meta['name'] +'/'+ gerenmames[i]
            yield Request(gerenurl,callback=self.get_mmurl,meta={'name':gerenmame})

    def get_mmurl(self,response):
        base_url = response.url[:-5]
        yema = response.xpath('//div[@class="page"]/ul/li[1]/a/text()').re(r'共(.*?)页')[0]
        for i in range(1,int(yema)+1):
            mmurl = base_url + '_' + str(i) +'.html'
            mmname = response.meta['name']
            yield Request(mmurl,callback=self.get_info,meta={'name': mmname})

    def get_info(self,response):
        item = MmItem()
        urls = response.xpath('//p[@align="center"]/a/img/@src').extract()
        for i in range(len(urls)):
            url = urls[i]
            name = response.meta['name'] +'/'+ url.split('/')[-1]
            item['images_url'] = [url]
            item['images_path']= name[:-8]
            yield item

