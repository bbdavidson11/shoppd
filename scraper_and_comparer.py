import requests
from bs4 import BeautifulSoup
import lxml
from PIL import Image
from io import BytesIO
import torch
import clip
import time
from image_text_vectorizer import generate_text_vector, find_closest_images

model, preprocess = clip.load("ViT-B/32")

class Product:
    def __init__(self, image_url, image_vector):
        self.image_url = image_url
        self.image_vector = image_vector

# generates vector for image only
def generate_vector(image):
    image = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        image_features = model.encode_image(image)
    return image_features

def download_process_img(imgLink):
    response = requests.get(imgLink)
    image = Image.open(BytesIO(response.content))

    # use to view images - WARNING: Please lower the limit on how many items are webscraped or it'll show every image
    # image.show()

    return generate_vector(image)

def webScrape(inputText, store="Aritzia"):
    start_time = time.time()

    if store == "Aritzia":
        productDict = getAritzia()
    elif store == "HM":
        productDict = getHM()

    # to check webscrape runtime vvv
    # end_time = time.time()
    # print("final time for scraping: " + str(end_time - start_time) + " seconds")

    # return find_closest_images(productDict, inputText)


def getAritzia():
    
    url = "https://www.aritzia.com/us/en/clothing?lastViewed=500"
    html = requests.get(url)

    soup = BeautifulSoup(html.content, 'lxml')

    clothingContainer = soup.find_all('div', class_="product-image ar-product-image js-product-plp-image tc js-product-plp-image--trigger-qv", limit=500)
    # note: first few are usually placeholder images - so useless to us
    clothingContainer = clothingContainer[10:]

    productDict = {}

    for clothing in clothingContainer:
        imgLink = clothing.find('img')["data-mouseover-img"]
        img = download_process_img(imgLink)

        productLink = clothing.find('a')["href"]

        productDict[productLink] = img

    return productDict

def getHM():
    print("got to H&M")
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    url = "https://www2.hm.com/en_us/women/new-arrivals/view-all.html"
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, 'lxml')

    # used to debug - uncomment to save a the html page that's retrieved and try to scrape using it as reference
    # with open("scraped_page.html", "w", encoding="utf-8") as file:
    #     file.write(soup.prettify())

    clothingContainer = soup.find("a", class_="db7c79")







if __name__ == "__main__":
    vectorizedText = generate_text_vector("a green tank top")
    webScrape(vectorizedText, "HM")

