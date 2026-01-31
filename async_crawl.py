import asyncio
import aiohttp
from urllib.parse import urlparse, urljoin
from crawl import *

class AsyncCrawler:
    def __init__(self, base_url, max_pages=25, max_concurrency=4):

        print(f"[init] base={base_url}, max_concurrency={max_concurrency} ({type(max_concurrency)})")

        self.base_url = base_url

        url = urlparse(base_url)
        self.base_domain = url.netloc

        self.page_data = {}       
        self.max_pages = max_pages
        self.max_concurrency = max_concurrency
        self.should_stop = False
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        # safely read/write self.page_data
        async with self.lock:
            if self.should_stop:
                return False
            
            if normalized_url in self.page_data:
                return False
            
            Npages = len(self.page_data)
            if Npages >= self.max_pages:
                self.should_stop = True
                print(f"Hit {Npages} of {self.max_pages} allowed pages to crawl.")
                for task in self.all_tasks:
                    if not task.done():
                        task.cancel()
                return False
            
            # self.page_data[normalized_url] = None
            # print(f"[add_page_visit] new: {normalized_url} (total={len(self.page_data)})")
            return True
    
    async def get_html(self, url):
        # safely limit concurrent requests
        async with self.session.get(
            url,
            headers={"User-Agent": "Bootscraper/1.0"},
            timeout=10,
        ) as resp:
            if resp.status >= 400:
                print(f"HTTP error when scraping boots (Status Code {resp.status}: {resp.reason}).")
                #  Exception as e:
                #     raise Exception(f"Something went wrong ({e}) with {url}. Try picking yourself up by your bootsraps?")
                return ""

            content_type = resp.headers.get('Content-Type','')
            # print(f" --> Found {content_type} as content type.")

            if "text/html" not in content_type:
                print(f"Page header type ({content_type}) inconsistent with scraping.")
                return ""
        
            return await resp.text()

    async def crawl_page(self, current_url):

        if self.should_stop:
            print("Reached max_limit in crawl_page. Returning now.")
            return
        
        url_domain = urlparse(current_url)

        if self.base_domain != url_domain.netloc:
            print(f"[crawl_page] Current url ({current_url}) exists outside of base url ({self.base_domain}).")
            return
    
        norm_url = normalize_url(current_url)
        is_new = await self.add_page_visit(norm_url)
        # print(f"[crawl_page] visited check: {current_url} -> {is_new}")
        if not is_new:
            # print("[crawl_page] Already crawl/ed this page. Moving on...")
            return

        # Semaphore limits how many crawls are in the “expensive” section at once.
        # If a parent holds the semaphore while awaiting children that also need it, you can deadlock at max_concurrency=1.
        # So: acquire semaphore → fetch/parse/store → release semaphore → then await children.
        async with self.semaphore:
            # print(f"[crawl_page] fetching: {current_url}")
            html = await self.get_html(current_url)
            # print(f"[crawl_page] got html: {current_url}, length={len(html) if html else 'None'} bytes")
            if not html:
                return
            my_page_data = extract_page_data(html, current_url)

            async with self.lock:
                self.page_data[norm_url] = my_page_data
                # print(f"[STORE] now have {len(self.page_data)} pages stored; just stored {current_url}")

            outgoing_links = my_page_data["outgoing_links"]
            # print(f"[crawl_page] {current_url} -> {len(outgoing_links)} links")

        tasklist = []
        for link in outgoing_links:
            parsed = urlparse(link)
            if parsed.scheme not in ("http", "https"):
                # print(f"[crawl_page] {parsed.scheme} is not http/https. Moving on...")
                continue
            if parsed.netloc != self.base_domain:
                continue

            async def safe_crawl(u):
                try:
                    await self.crawl_page(u)
                except Exception as e:
                    print(f"[crawl_page] ERROR while crawling {u}: {e}")

            task = asyncio.create_task(safe_crawl(link))
            tasklist.append(task)
            self.all_tasks.add(task)
            # print(f"all_tasks contains {len(self.all_tasks)} entries.")

        if tasklist:
            # print(f"[crawl_page] awaiting {len(tasklist)} children for {current_url}")
            try:
                await asyncio.gather(*tasklist, return_exceptions=True)
            finally:
                for task in tasklist:
                    self.all_tasks.discard(task)


        # print(f"[crawl_page] done: {current_url}")
        return

    async def crawl(self):
        # print("[crawl] starting")
        await self.crawl_page(self.base_url)
        # print("[crawl] done")
        print(f"[crawl] collected {len(self.page_data)} pages")
        return self.page_data
    
async def crawl_site_async(base_url, max_pages, max_concurrency):
    acrawler = AsyncCrawler(base_url, max_pages, max_concurrency)
    async with acrawler:
        page_data = await acrawler.crawl()
        return page_data
    
