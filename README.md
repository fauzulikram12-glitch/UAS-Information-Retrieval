# UAS Information Retrieval (SIF502)

Web scraping dan pencarian buku menggunakan Scrapy + Streamlit.

## Tech Stack

- **Scrapy** — scraping data buku dari [books.toscrape.com](http://books.toscrape.com) ([GitHub](https://github.com/fauzulikram12-glitch/UAS-Information-Retrieval))
- **Streamlit** — Web UI untuk pencarian/filter buku ([Live App](https://uas-information-retrieval-wafzie3tt6ywt2wkgomhex.streamlit.app/))
- **Pandas** - Data processing

## Project Structure

```
uas-information-retrieval/
├── app.py                    # Streamlit web UI
├── requirements.txt          # Python dependencies
├── scrapy.cfg                # Scrapy configuration
├── data/
│   └── books.json            # Data hasil scraping (1000 buku)
└── bookscraper/
    ├── __init__.py
    ├── items.py              # Scrapy Item definitions
    ├── middlewares.py        # Spider & downloader middlewares
    ├── pipelines.py         # JSON file writer pipeline
    ├── settings.py           # Scrapy settings
    └── spiders/
        ├── __init__.py
        └── books_spider.py   # Main spider
```

## Cara Menjalankan

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Web Scraping

```bash
cd uas-information-retrieval
scrapy crawl books
```

Data tersimpan di `data/books.json`.

### 3. Jalankan Web UI

```bash
streamlit run app.py
```

## Features

- Pencarian buku berdasarkan judul (real-time search)
- Filter berdasarkan harga (range slider)
- Filter berdasarkan rating (1-5 bintang)
- Filter berdasarkan ketersediaan (in stock / out of stock)
- Tabel hasil dengan link ke halaman buku

## Deployment (Streamlit Community Cloud)

1. Push repo ke GitHub (public)
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repo
4. Set `app.py` sebagai main file
5. Deploy

## License

Tugas UAS SIF502 - Information Retrieval
