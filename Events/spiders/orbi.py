from pathlib import Path

import scrapy

class OrbiSpider(scrapy.Spider):
    name = "orbi"
    start_urls = ["https://orbi.io/events?school=-KqgTRAYh2diOyp5pUPg"]

    def parse(self, response):
        for event in response.css('a[href^="/events/"]'):
            url = response.urljoin(event.attrib["href"])
            loc_p = event.css("p")[-1]
            location = loc_p.css("span:first-child::text").get("").strip()

            item = {
                "title": event.css("h3::text").get().strip(),
                "url": url,
                "date": event.css("time::attr(datetime)").get(),
                "tags": "none",
                "summary": "none",
                "location": location,
            }
            yield response.follow(url, callback=self.parse_detail, cb_kwargs={"item": item})


    def parse_detail(self, response, item):
        summary = response.css("section div span::text").get().strip()
        item["summary"] = summary
        yield item