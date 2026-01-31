import sys
import asyncio
from crawl import crawl_page
from async_crawl import crawl_site_async
from csv_report import write_csv_report

def main():    

    narg = len(sys.argv)

    if narg < 2:
        print("no website provided")
        sys.exit(1)
    elif narg > 6:
        print("too many arguments provided")
        sys.exit(1)

    base_url = sys.argv[1]
    max_concurrency = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
    max_pages = int(sys.argv[3]) if len(sys.argv) >= 4 else 100
    mode = sys.argv[4] if len(sys.argv) >= 5 else "async"
        
    # print("Starting crawl of: ", base_url)
    # print("Maximum concurrency: ", max_concurrency)
    # print("Maximum number of pages:", max_pages)
    # print("Mode set to: ", mode)
    
    if mode == "sync":
        print("Running bootscaper in sync mode...")
        main_sync(base_url)
    else:
        asyncio.run(main_async(base_url, max_pages, max_concurrency))
    
    # print(page_data)
    sys.exit(0)


def main_sync(base_url):
    page_data = crawl_page(base_url)
    print_report(page_data)
    return


async def main_async(base_url, max_pages=100, max_concurrency=5):
    page_data = await crawl_site_async(base_url, max_pages, max_concurrency)
    # print_report(page_data)
    write_csv_report(page_data)
    return


def print_report(page_data):
    print(f"Size of site is {len(page_data)} pages.")
    for i,page in enumerate(page_data.values(), start=1):
        if page:
            # print(f"Page {i}: {page['url']}")
            print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")


if __name__ == "__main__":
    main()
