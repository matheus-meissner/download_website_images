import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def get_all_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    background_images = [tag['style'] for tag in soup.find_all(style=True) if 'background-image' in tag['style']]
    
    img_urls = []

    for img in images:
        img_url = img.get('src')
        if img_url:
            img_urls.append(urljoin(url, img_url))

    for bg in background_images:
        url_start = bg.find('url(') + 4
        url_end = bg.find(')', url_start)
        img_url = bg[url_start:url_end].strip('\'"')
        img_urls.append(urljoin(url, img_url))

    return img_urls

def download_images(img_urls, folder='imagesy'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for img_url in img_urls:
        try:
            img_data = requests.get(img_url).content
            img_name = os.path.join(folder, img_url.split('/')[-1])
            with open(img_name, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded: {img_url}")
        except Exception as e:
            print(f"Could not download {img_url}: {e}")

if __name__ == "__main__":
    site_url = "https://worlds.pokemon.com/pt-br/"
    image_urls = get_all_images(site_url)
    download_images(image_urls)