import scrapy
import json
from ..items import NaukriItem
from scrapy.loader import ItemLoader


class RemoteJobsSpider(scrapy.Spider):
    name = "remote_jobs"
    allowed_domains = ["naukri.com"]
    start_urls = [
        'https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=adv&keyword=remote&pageNo=1&seoKey=remote-jobs&src=discovery_trendingWdgt_homepage_srch&latLong=']

    def parse(self, response):
        payload = json.loads(response.body)
        for j in payload['jobDetails']:
            i = ItemLoader(item=NaukriItem)
            i.add_value('title', j['title'])
            i.add_value('company', j['companyName'])
            i.add_value('description', j['jobDescription'])
            i.add_value('location', \
                        (x['label'] \
                            for x in j['placeholders'] \
                                if x['type'] == 'location'))
            i.add_value('date', j['createdDate'])
            yield i.load_item()
