import requests
from bs4 import BeautifulSoup
import lxml
from PIL import Image
from io import BytesIO
import torch
import clip


model, preprocess = clip.load("ViT-B/32")

class Product:
    def __init__(self, image_url, image_vector):
        self.image_url = image_url
        self.image_vector = image_vector


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


if __name__ == "__main__":

    url = "https://www.aritzia.com/us/en/clothing?lastViewed=100"
    html = requests.get(url)

    soup = BeautifulSoup(html.content, 'lxml')

    clothingContainer = soup.find_all('div', class_="product-image ar-product-image js-product-plp-image tc js-product-plp-image--trigger-qv", limit=20)
    # note: first few are usually placeholder images - so useless to us
    clothingContainer = clothingContainer[10:]


    for clothing in clothingContainer:
        imgLink = clothing.find('img')["data-mouseover-img"]
        img = download_process_img(imgLink)


        link = clothing.find('a')["href"]

