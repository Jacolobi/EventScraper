from pathlib import Path

import scrapy

class NkpgSpider(scrapy.Spider):
    name = "nkpg"
    base_url = "https://visit.norrkoping.se/se-och-gora/evenemangskalender"

    async def start(self):
        yield scrapy.Request(f"{self.base_url}?query=&page=1", cb_kwargs={"page": 1})

    def parse(self, response, page):
        events = response.css("a.vn-search__hit-link")
        for event in events:
            url = response.urljoin(event.attrib["href"])

            item = {
                "title": event.attrib["title"],
                "url": url,
                "date": event.css("div.vn-search__hit-image-event-date::text").get().strip(),
            }

            yield response.follow(url, callback=self.parse_detail, cb_kwargs={"item": item})

        if events:
            next_page = page + 1
            yield scrapy.Request(
                f"{self.base_url}?query=&page={next_page}",
                callback=self.parse,
                cb_kwargs={"page": next_page},
            )


    def parse_detail(self, response, item):
        summary = response.css("p.vn-ingress::text").get().strip()
        location = None
        for box in response.css("div.vn-object-page__information-box-metadata-item"):
            title = " ".join(box.css("div.vn-object-page__information-box-metadata-item-title ::text").getall()).strip()
            if title == "Adress":
                location = " ".join(
                    t.strip() for t in box.css("div.vn-object-page__information-box-metadata-item-value ::text").getall() if t.strip()
                ) or None
                break
        item["summary"] = summary
        item["location"] = location
        item["category"] = None
        item["requires_booking"] = None
        item["restricted"] = None
        yield item