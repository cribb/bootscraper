# Bootscraper (boot.dev guided project)

## Sync → Async mapping:

    page_data dict → self.page_data on AsyncCrawler
    crawl_page(base_url, current_url, page_data) → async def crawl_page(self, current_url)
    visited check:
        sync: if norm_url in page_data: ...
        async: is_new = await self.add_page_visit(norm_url); if not is_new: return
    fetch:
        sync: html = get_html(current_url)
        async: async with self.semaphore: html = await self.get_html(current_url)
    store:
        sync: page_data[norm_url] = extract_page_data(...)
        async: async with self.lock: self.page_data[norm_url] = extract_page_data(...)
    recurse:
        sync: page_data = crawl_page(... link ...)
        async: tasks.append(asyncio.create_task(self.crawl_page(link))); await asyncio.gather(*tasks)
