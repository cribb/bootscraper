import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def normalize_url(url):
    purl = urlparse(url)
    # print(f"urlinfo: {purl}")
    outurl = f"{purl.netloc}{purl.path}".rstrip("/")
    # print(f"outurl: {outurl}")
    return outurl

def get_h1_from_html(html):
    soup = BeautifulSoup(html, "html.parser")

    if soup is not None and soup.h1:
        h1str = soup.h1.string
    else:
        h1str = ""
    
    # print(f"h1str: {h1str}")
    return h1str

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, "html.parser")

    if soup is not None:
        if soup.main is not None and soup.main.p:
            pstr = soup.main.p.string.strip(" ")
        elif soup.p is not None and soup.p.string:
            pstr = soup.p.string.strip(" ")
        else:
            pstr = ""
    
    # print(f"pstr: {pstr}")
    return pstr

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    if not soup:
        return ""
    
    a_tags = soup.find_all("a")
    # links = list(map(lambda x:x.get("href"), a_tags))

    urls = []
    for tag in a_tags:
        purl = urlparse(tag.get("href"))
        urls.append(urljoin(base_url, purl.path))
    
    return urls

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    if not soup:
        return ""
    
    img_tags = soup.find_all("img")

    imgurls = []
    for tag in img_tags:
        imgurl = tag.get("src")
        imgurls.append(urljoin(base_url, imgurl))
    
    return imgurls


def extract_page_data(html, page_url):    
    page = {}
    page["url"] = page_url
    page["h1"] = get_h1_from_html(html)
    page["first_paragraph"] = get_first_paragraph_from_html(html)
    page["outgoing_links"] = get_urls_from_html(html, page_url)
    page["image_urls"] = get_images_from_html(html, page_url)
    # print(f"Page: {page}")
    return page

def get_html(url):
    r = requests.get(url, headers={"User-Agent": "Bootscraper/1.0"})
    content_type = r.headers['Content-Type']
    print(content_type)

    if r.status_code >= 400:
        sys.exit(f"Error when scraping boots (Status Code {r.status_code}: {r.reason}).")
    
    if "text/html" not in content_type:
        sys.exit(f"Error with header info.")
    
    return r.text

def crawl_page():
    pass

def main():    

    html = "Well, well, <h1>Karen Walker.</h1> \n<p>Beverly Leslie.</p>"
    h1 = get_h1_from_html(html)
    p = get_first_paragraph_from_html(html)
    print(f"h1: {h1}")
    print(f" p: {p}")


if __name__ == "__main__":
    main()

