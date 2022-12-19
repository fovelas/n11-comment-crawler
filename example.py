from n11_crawler import N11Crawler

crawler = N11Crawler("561281932", save_as_json=False, max_comments=10, progress_bar=True)
crawler.run()

print(crawler.get_comments()[0]["date"])
print(crawler.get_page_count())
print(crawler.get_fetch_time())
print(crawler.get_comments_length())
print(crawler.save_as_json(filename="yorumlar"))