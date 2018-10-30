import scrapy
import json
from urllib.parse import urljoin

class shakespeareSpider(scrapy.Spider):
    name = "shakespeare"
    start_urls = ['https://www.litcharts.com/shakescleare/shakespeare-translations']
    # # start_urls = ['https://www.litcharts.com/shakescleare/shakespeare-translations/henry-vi-part-2/act-5-scene-1']
    # start_urls = ['https://www.litcharts.com/shakescleare/shakespeare-translations/henry-vi-part-1/act-4-scene-6']
    # previous_texts = []


    def parse(self, response):
        base_url = 'https://www.litcharts.com'
        next_pages = response.css('a.translation.hoverable::attr(href)').extract()
        print('*' * 80, len(next_pages))
        for relative_url in next_pages:
            print(relative_url)
            url = urljoin(base_url, relative_url)
            print(url)
            yield scrapy.Request(url = url, callback = self.parse_book_url)

    def parse_book_url(self, response):
        base_url = 'https://www.litcharts.com'
        next_pages = response.css('div.table-of-contents a::attr(href)').extract()
        print('*' * 80)
        for relative_url in next_pages:
            url = urljoin(base_url, relative_url)
            print(url)
            yield scrapy.Request(url = url, callback = self.parse_chapters)

    def parse_chapters(self, response):
        original_texts = {}
        for original in response.css('.original-content .shakespeare-translation-line'):
            if len(original.css('span[data-id]')) == 0:
                continue
            span_nodes = original.css('span[data-id]')
            for i in range(len(span_nodes)):
                data_id = span_nodes[i].css('::attr(data-id)').extract_first()
                text = span_nodes[i].css('::text').extract_first()
                if text == None:
                    continue
                if data_id not in original_texts:
                    original_texts[data_id] = []
                text = ''.join(filter(lambda c: 0 <= ord(c) and ord(c) <= 255, text)) # get ride of unicode chars
                original_texts[data_id].append(text)

        translated_texts = {}
        for translated in response.css('div.translation-content p.speaker-text'):
            if len(translated.css('span[data-id]')) == 0:
                continue
            span_nodes = translated.css('span[data-id]')
            for i in range(len(span_nodes)):
                data_id = span_nodes[i].css('::attr(data-id)').extract_first()
                text = span_nodes[i].css('::text').extract_first()
                if text == None:
                    continue
                if data_id not in translated_texts:
                    translated_texts[data_id] = []
                text = ''.join(filter(lambda c: 0 <= ord(c) and ord(c) <= 255, text)) # get ride of unicode chars
                translated_texts[data_id].extend(text)

        for data_id in original_texts:
            if data_id in translated_texts:
                yield {
                    'original': "".join(original_texts[data_id]),
                    'translated': "".join(translated_texts[data_id]),
                }

