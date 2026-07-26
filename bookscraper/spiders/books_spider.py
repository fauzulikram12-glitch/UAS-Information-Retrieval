import scrapy
from bookscraper.items import BookItem


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        for article in response.css("article.product_pod"):
            item = BookItem()

            item["title"] = article.css("h3 a::attr(title)").get()
            item["price"] = article.css(".price_color::text").get()
            item["rating"] = RATING_MAP.get(
                article.css("p.star-rating::attr(class)").get("").split()[-1], 0
            )
            item["availability"] = " ".join(
                t.strip() for t in article.css(".availability ::text").getall() if t.strip()
            )
            item["link"] = response.urljoin(
                article.css("h3 a::attr(href)").get()
            )

            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
