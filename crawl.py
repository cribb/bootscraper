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

    if not soup:
        print("Soup not found :/.")
        return ""
    
    if soup.find("main"):
        pstr = soup.find("p")
    else:
        pstr = soup.find("p")
    
    # print(f"pstr: {pstr}")
    if pstr:
        return pstr.get_text(strip=True)
    return ""

# def get_first_paragraph_from_html(html):
#     soup = BeautifulSoup(html, "html.parser")

#     if not soup:
#         print("Soup not found :/.")
#         return ""

#     if soup.main and soup.main.p:
#         pstr = soup.main.p.string.strip(" ")
#     elif soup.p and soup.p.string:
#         pstr = soup.p.string.strip(" ")
#     else:
#         pstr = ""   
#     # print(f"pstr: {pstr}")
#     return pstr

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    if not soup:
        return ""
    
    a_tags = soup.find_all("a")
    # links = list(map(lambda x:x.get("href"), a_tags))

    urls = []
    for tag in a_tags:
        if href := tag.get("href"):
            try:
                url = urljoin(base_url, href)
                urls.append(url)
            except Exception as e:
                print(f"{str(e)}: {href}")

    return urls

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    img_tags = soup.find_all("img")

    imgurls = []
    for tag in img_tags:
        if src := tag.get("src"):
            try:
                imgurl = urljoin(base_url, src)
                imgurls.append(urljoin(base_url, imgurl))
            except Exception as e:
                print(f"{str(e)}: {src}")
    
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

    try:
        resp = requests.get(url, headers={"User-Agent": "Bootscraper/1.0"})
    except Exception as e:
        print(f"Something went wrong ({e}) with {url}. Try picking yourself up by your bootsraps?")
        return

    if resp.status_code >= 400:
        print(f"HTTP error when scraping boots (Status Code {resp.status_code}: {resp.reason}).")
        return

    content_type = resp.headers['Content-Type']
    print(f" --> Found {content_type} as content type.")

    if "text/html" not in content_type:
        print(f"Page header type ({content_type}) inconsistent with scraping.")
        return
    
    return resp.text

def crawl_page(base_url, current_url=None, page_data=None):

    if current_url is None:
        current_url = base_url

    if page_data is None:
        page_data = {}

    parsed_base = urlparse(base_url)
    parsed_current = urlparse(current_url)

    if parsed_base.netloc != parsed_current.netloc:
        print(f"Current url ({current_url}) exists outside of base url ({base_url}). Returning empty-handed.")
        return page_data

    norm_url = normalize_url(current_url)

    if norm_url in page_data:
        print(" --> Already crawled this page. Moving on...")
        return page_data
    
    # norm_url is appropriate for dictionary entry, but not as an actual link
    html = get_html(current_url)
    
    if not html:
        return
    
    # print(html)
    page_data[norm_url] = extract_page_data(html, current_url)

    outgoing_links = page_data[norm_url]["outgoing_links"]
    # unique_list_of_links = list(set(outgoing_links))

    for link in outgoing_links:
        print(f"Plumbing the depths of {link}...")
        page_data = crawl_page(base_url, current_url=link, page_data=page_data)
        
    return page_data



def main():    
    html = "Well, well, <h1>Karen Walker.</h1> \n<p>Beverly Leslie.</p>"
    h1 = get_h1_from_html(html)
    p = get_first_paragraph_from_html(html)
    print(f"h1: {h1}")
    print(f" p: {p}")


if __name__ == "__main__":
    main()

