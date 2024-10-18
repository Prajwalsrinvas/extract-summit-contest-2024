# zyte_spider_templates_project/spiders/custom_ecommerce_spider.py

from typing import Iterable

from scrapy import Request
from scrapy_poet import DummyResponse
from zyte_common_items import Product
from zyte_spider_templates import EcommerceSpider


class CustomEcommerceSpider(EcommerceSpider):
    name = "custom_ecommerce_spider"

    custom_settings = {
        "ZYTE_API_TRANSPARENT_MODE": True,
        "ZYTE_API_AUTOMAP": True,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_url = kwargs.get(
            "url",
            "https://zzcvcpnfzoogpxiqupsergvrmdopqgrk-744852047878.us-south1.run.app/navigation",
        )
        self.extract_from = "httpResponseBody"

    def start_requests(self) -> Iterable[Request]:
        yield Request(url=self.start_url, callback=self.parse_navigation)

    def parse_navigation(self, response):
        product_links = response.css("a::attr(href)").getall()
        for link in product_links:
            full_url = response.urljoin(link)
            yield Request(url=full_url, callback=self.parse_product)

    def parse_product(
        self, response: DummyResponse, product: Product
    ) -> Iterable[dict]:
        yield {
            "url": str(product.url) if hasattr(product, "url") else None,
            "name": product.name if hasattr(product, "name") else None,
            "brand": (
                product.brand.name
                if hasattr(product, "brand")
                and product.brand
                and hasattr(product.brand, "name")
                else None
            ),
            "sku": product.sku if hasattr(product, "sku") else None,
            "price": (
                str(product.price)
                if hasattr(product, "price") and product.price is not None
                else None
            ),
            "rating": (
                float(product.aggregateRating.ratingValue)
                if hasattr(product, "aggregateRating")
                and product.aggregateRating
                and hasattr(product.aggregateRating, "ratingValue")
                and product.aggregateRating.ratingValue is not None
                else None
            ),
            "reviews": (
                int(product.aggregateRating.reviewCount)
                if hasattr(product, "aggregateRating")
                and product.aggregateRating
                and hasattr(product.aggregateRating, "reviewCount")
                and product.aggregateRating.reviewCount is not None
                else None
            ),
        }
