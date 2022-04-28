import scrapy
from scrapy.http import FormRequest, JsonRequest


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['www.httpbin.org']
    start_url = 'https://www.httpbin.org/post'
    data = {'name': 'germey', 'age': 'age'}

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Aoyou/P09NOgtIRVIldAkvIUlifmi22nrQKYQzad434AaGuhhjAUCu8XZgurGV-A=='
    # }
    # cookies = {
    #     'name': 'germey',
    #     'age': 'age'
    # }

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield Request(url, dont_filter=True)

    # def start_requests(self):
    #     for offset in range(5):
    #         url = self.start_url + f'?offset={offset}'
    #         yield Request(url, headers=self.headers, cookies=self.cookies, callback=self.parse_response,
    #                       meta={'offset': offset})

    def start_requests(self):
        yield FormRequest(self.start_url, callback=self.parse_response, formdata=self.data)
        yield JsonRequest(self.start_url, callback=self.parse_response, data=self.data)

    def parse_response(self, response):
        print('text', response.text)

    # def parse_response(self, response):
    #     print('url', response.url)
    #     print('request', response.request)
    #     print('status', response.status)
    #     print('headers', response.headers)
    #     print('text', response.text)
    #     print('meta', response.meta)
