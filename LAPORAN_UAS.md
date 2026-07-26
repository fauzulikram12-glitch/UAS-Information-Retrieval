# LAPORAN UAS - Information Retrieval (SIF502)

## Web Scraping dan Pencarian Buku dengan Scrapy dan Streamlit

---

## 1. Pendahuluan

### 1.1 Latar Belakang

Information Retrieval (IR) adalah ilmu yang mempelajari cara mengumpulkan, mengorganisasi, dan mencari informasi dari berbagai sumber data. Dalam era digital, kemampuan untuk melakukan web scraping dan menyediakan mekanisme pencarian yang efektif menjadi sangat penting.

Proyek ini bertujuan untuk menerapkan konsep Information Retrieval dalam tiga tahap utama:

1. **Web Scraping** menggunakan framework Scrapy untuk mengumpulkan data buku dari situs [books.toscrape.com](http://books.toscrape.com)
2. **Penyimpanan Data** dalam format JSON sebagai intermediate storage
3. **Pembuatan Web UI** menggunakan Streamlit untuk pencarian dan filter data buku

### 1.2 Tujuan

- Menerapkan teknik web scraping menggunakan Scrapy
- Membangun pipeline data dari scraping hingga penyimpanan
- Membangun antarmuka pencarian yang user-friendly dengan Streamlit
- Mengoreksi bug logika pada draf kode soal

---

## 2. Analisis dan Perancangan

### 2.1 Target Scraping

Target scraping adalah website [books.toscrape.com](http://books.toscrape.com/catalogue/page-1.html), sebuah website sandbox yang dirancang khusus untuk latihan web scraping.

**Struktur HTML target:**

```html
<article class="product_pod">
    <h3><a href="..." title="Book Title">Book Title</a></h3>
    <p class="star-rating Three">
        <i class="icon-star"></i> ...
    </p>
    <div class="product_price">
        <p class="price_color">£51.77</p>
        <p class="instock availability">
            <i class="icon-ok"></i>
            In stock
        </p>
    </div>
</article>
```

**Field yang di-scrape:**

| Field | CSS Selector | Keterangan |
|-------|-------------|------------|
| `title` | `h3 a::attr(title)` | Judul buku |
| `price` | `.price_color::text` | Harga (£) |
| `rating` | `p.star-rating::attr(class)` | Rating (1-5) |
| `availability` | `.availability ::text` | Status stok |
| `link` | `h3 a::attr(href)` | URL halaman buku |

### 2.2 Bug Logika yang Diperbaiki

Draf kode soal awal menggunakan field `quote` dan `author`, yang tidak sesuai dengan struktur data target (buku, bukan kutipan). Perbaikan dilakukan:

- **Sebelum (bug):** Field `quote`, `author`
- **Sesudah (benar):** Field `title`, `price`, `rating`, `availability`, `link`

---

## 3. Implementasi

### 3.1 Struktur Proyek

```
uas-information-retrieval/
├── app.py                    # Streamlit Web UI
├── requirements.txt          # Dependencies
├── scrapy.cfg                # Scrapy config
├── data/
│   └── books.json            # 1000 data buku
└── bookscraper/
    ├── items.py              # Data model
    ├── pipelines.py          # JSON writer
    ├── settings.py           # Scrapy settings
    └── spiders/
        └── books_spider.py   # Spider utama
```

### 3.2 Scrapy Spider (`books_spider.py`)

Spider menggunakan class `BooksSpider` yang mewarisi `scrapy.Spider`:

```python
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
                t.strip() for t in article.css(".availability ::text").getall()
                if t.strip()
            )
            item["link"] = response.urljoin(article.css("h3 a::attr(href)").get())
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

**Penjelasan:**

1. **CSS Selector:** Digunakan untuk mengekstrak data dari HTML
2. **Rating Mapping:** Konversi teks "One","Two",... menjadi angka 1-5
3. **Pagination:** Spider otomatis mengikuti link "next" hingga semua halaman selesai
4. **Availability Bug Fix:** Menggunakan `getall()` untuk mengambil semua text nodes dan filter yang non-kosong, karena text "In stock" bukan text node pertama

### 3.3 Scrapy Pipeline (`pipelines.py`)

Pipeline menulis semua item ke file JSON:

```python
class JsonWriterPipeline:
    def open_spider(self, spider):
        self.items = []
        # Buat direktori data/ jika belum ada

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
```

Pipeline diaktifkan di `settings.py`:

```python
ITEM_PIPELINES = {
    "bookscraper.pipelines.JsonWriterPipeline": 300,
}
```

### 3.4 Streamlit Web UI (`app.py`)

Aplikasi Streamlit menyediakan fitur:

1. **Pencarian Judul:** Text input dengan pencarian case-insensitive
2. **Filter Harga:** Range slider dari harga minimum ke maksimum
3. **Filter Rating:** Multi-select rating 1-5 bintang
4. **Filter Availability:** Multi-select status stok
5. **Tabel Hasil:** Menampilkan data yang sudah difilter dalam format markdown

**Kode utama filtering:**

```python
filtered = df[
    (df["title"].str.contains(search_title, case=False, na=False))
    & (df["price_num"] >= price_range[0])
    & (df["price_num"] <= price_range[1])
    & (df["rating"].isin(selected_ratings))
    & (df["availability"].isin(selected_availability))
]
```

---

## 4. Hasil

### 4.1 Hasil Scraping

- **Total buku:** 1000 item
- **Total halaman:** 50 halaman
- **Waktu scraping:** ~22 detik
- **Format output:** JSON (data/books.json)

**Contoh data:**

```json
{
    "title": "A Light in the Attic",
    "price": "£51.77",
    "rating": 3,
    "availability": "In stock",
    "link": "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
}
```

### 4.2 Web UI

Streamlit app berjalan di `localhost:8501` dengan fitur pencarian dan filter real-time.

---

## 5. Deployment

### 5.1 GitHub

1. Inisialisasi Git repository
2. Push semua file ke GitHub (public repo)
3. Pastikan `data/books.json` ter-commit

### 5.2 Streamlit Community Cloud

1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Authorize dengan GitHub
3. Pilih repository
4. Set main file path: `app.py`
5. Klik "Deploy"

---

## 6. Kesimpulan

Proyek ini berhasil menerapkan konsep Information Retrieval melalui:

1. **Web Scraping** dengan Scrapy yang efisien dan terstruktur
2. **Data Pipeline** dari HTML mentah ke JSON yang terorganisir
3. **Web Interface** dengan Streamlit yang mendukung pencarian multi-kriteria
4. **Bug Fix** pada ketidakcocokan field data (quote/author -> title/price/rating/availability/link)

Hasil akhir berupa aplikasi web yang dapat di-deploy ke Streamlit Community Cloud untuk akses publik.

---

## 7. Daftar Pustaka

- Scrapy Documentation: https://docs.scrapy.org
- Streamlit Documentation: https://docs.streamlit.io
- Books to Scrape: http://books.toscrape.com
