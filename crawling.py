import requests
from bs4 import BeautifulSoup

def crawl_pages(base_url, total_pages):
    for page_num in range(1, total_pages + 1):
        url = f"{base_url}/{page_num}/"
        print(f"Crawling page {page_num}...")
        data = crawl_links(url)

def crawl_links(url):
    results = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', class_='news-item__title')
            for link in links:
                href = link.get('href')
                if href:
                    results.append(getpage(href, base_url))  
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

    return results

def getpage(link, base_url):
    result = {'Link': link}
    try:
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            tanggal = soup.find("time", class_="posted-on entry-date published updated")
            tanggal_text = tanggal.get_text(strip=True) if tanggal else ""
            
            judul = soup.find("h1", class_="page-title topper__title news")
            judul_text = judul.get_text(strip=True) if judul else ""
            
            content = soup.find(class_="body-content")
            content_text = ""
            if content:
                paragraphs = content.find_all("p")
                content_text = "\n".join(paragraph.get_text(strip=True) for paragraph in paragraphs).replace('\n', '')
            result.update({'Tanggal': tanggal_text, 'Judul': judul_text, 'Content': content_text})
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return result

base_url = "" #homepage web
total_pages = 1 # adjusted to the number of web pages

crawl_pages(base_url, total_pages)
