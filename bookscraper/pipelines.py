import json
import os


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.items = []
        self.output_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data",
            "books.json",
        )
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
        spider.logger.info(f"Saved {len(self.items)} items to {self.output_path}")
