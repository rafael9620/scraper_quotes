import scrapy
# Titulos = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page button = //ul[@class="pager"]//li[@class="next"]/a/@href


class ScraperQuotes(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
    ]

    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUEST': 24,
        'MEMUSAGE_LIMIT_MB':2048,
        'MEMUSAGE_NOTIFY_MAIL':['franciscoreg@uci.cu'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT':'Francisco R',
        'FEED_EXPORT_ENCODING': 'utf-8'

    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
        
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]//li[@class="next"]/a/@href').get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})

        else:
            yield{
                'quotes': quotes
            }

        

    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        top_ten_tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        yield {
            'title': title,

            'top_ten_tags': top_ten_tags

        }

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]//li[@class="next"]/a/@href').get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
