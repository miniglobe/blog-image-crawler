# -*- coding: utf-8 -*-
import scrapy
from gunosynews.items import GunosynewsItem


class GunosySpider(scrapy.Spider):
    name = 'gunosy'
    allowed_domains = ['gunosy.com']

    # 起点となるURL
    start_urls = ["https://gunosy.com/categories/1"]

    def parse(self, response):

        for href in response.css("div.list_content"):
            url = href.css("div.list_title > a::attr('href')").extract_first()
            #article['url'] = sel.css("div.list_title > a::attr('href')").extract_first()
            #crawl(article)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    
        next_page = response.css("div.pager-link-option > a::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, callback=self.parse)
    
    def parse_dir_contents(self, response):
        items = GunosynewsItem()
        items["title"] = response.css('.article_header_title::text').extract_first()
        items["image"]  = response.css('.article__image > img::attr(data-src)').extract_first()
        items["text"] = ''.join(response.css('.article > p::text').extract())
        items['url'] = response.url
        return items

