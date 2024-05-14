import requests
from bs4 import BeautifulSoup
import lxml
from PIL import Image
from io import BytesIO
import torch
import clip
import time
from image_text_vectorizer import generate_text_vector, find_closest_images
import store_retrieve_vectors

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
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

    response = requests.get(imgLink, headers=headers)
    image = Image.open(BytesIO(response.content))

    # use to view images - WARNING: Please lower the limit on how many items are webscraped or it'll show every image
    # image.show()

    return generate_vector(image)

def webScrape(inputText, store="Aritzia"):
    start_time = time.time()

    # this try-catch statement basically tries to get the last time this store was scraped
    # if it was last scraped more than a week ago, then we'll update the vectors - since the clothes might be out of stock
    # if it was never scraped (which we'll catch here), then we'll just set time to 0
    try:
        last_scrape = store_retrieve_vectors.getTime(store)
    except:
        last_scrape = 0

    print("current time: " + str(start_time))
    print("last scrape occured on" + str(last_scrape))
    
    if start_time - last_scrape > (24*60*60*7):
        if store == "Aritzia":
            result = getAritzia(inputText)
        elif store == "Lacoste":
            result = getLacoste(inputText)
        elif store == "Abercrombie":
            result = getAbercrombie(inputText)
        elif store == "Tom Ford":
            result = getTomFord(inputText)

        store_retrieve_vectors.storeTo(store, result)
    else:
        result = store_retrieve_vectors.getVectors(store)

    topMatches = find_closest_images(result, inputText)

    end_time = time.time()
    print("final time for scraping: " + str(end_time - start_time) + " seconds")

    # return result
    return topMatches


def getAritzia(inputText):
    
    url = "https://www.aritzia.com/us/en/clothing?lastViewed=1000"
    html = requests.get(url)

    soup = BeautifulSoup(html.content, 'lxml')

    clothingContainer = soup.find_all('div', class_="product-image ar-product-image js-product-plp-image tc js-product-plp-image--trigger-qv", limit=1000)
    # note: first few are usually placeholder images - so useless to us
    clothingContainer = clothingContainer[10:]

    productDict = {}

    for clothing in clothingContainer:
        imgLink = clothing.find('img')["data-mouseover-img"]
        img = download_process_img(imgLink)

        productLink = clothing.find('a')["href"]

        productDict[productLink] = img

    # return find_closest_images(productDict, inputText)
    return productDict

def getLacoste(inputText):
    print("got to Lacoste")
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

    urlBaseWomen = "https://www.lacoste.com/us/lacoste/women/clothing/?sortBy=lc_t2s_rank1&page="
    urlBaseMen = "https://www.lacoste.com/us/lacoste/men/clothing/?sortBy=lc_t2s_rank1&page="

    baseLinks = [urlBaseWomen, urlBaseMen]

    productDict = {}

    # note: each page has 36 items (as of 5/11/24), and the following loop will do it the specified number of times for both men and woman pages
    # The formula for the number of pages scraped is: 2 * (num - 1) * 32
    # make sure num >= 2 and you don't exceed # of pages Lacoste
    numLoops = 8
    for urlBase in baseLinks:
        for y in range (1, numLoops):
            currUrl = urlBase + str(y)
            html = requests.get(currUrl, headers=headers)
            soup = BeautifulSoup(html.content, 'lxml')

            clothingContainer = soup.find_all('a', class_="js-product-tile-link l-relative no-user-select")

            for clothing in clothingContainer:
                productLink = clothing["href"]

                imgLink = "https:" + clothing.find('img')["data-alternate-src"]
                img = download_process_img(imgLink)

                productDict[productLink] = img



            # used to debug - uncomment to save a the html page that's retrieved and try to scrape using it as reference
            # put this inside the loop or write a simple code to request url
            # with open("scraped_page.html", "w", encoding="utf-8") as file:
            #     file.write(soup.prettify())

    return productDict

def getAbercrombie(inputText):
    baseMenURL = "https://www.abercrombie.com/shop/us/mens?filtered=true&rows=90&start="
    baseWomenURL = "https://www.abercrombie.com/shop/us/womens?filtered=true&rows=90&start="

    baseURLs = [baseMenURL, baseWomenURL]

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

    productDict = {}
    topVectors = []

    # Note: each page has 90 images, which is what the URL goes off of
    # numLoops = 2
    numLoops = 3
    for url in baseURLs:
        for y in range (0, numLoops):
            html = requests.get(url + str(y * 90), headers=headers)
            soup = BeautifulSoup(html.content, 'lxml')
            
            # Each product card has the specific attribute "data-aui" with the value "product-card"
            clothingContainer = soup.find_all('li', {"data-aui":"product-card"})

            for clothing in clothingContainer:
                productLink = "https://www.abercrombie.com" + clothing.find('a')["href"]

                # There's a js file called "getImageUrl.js" that defines how their image urls are made
                imgID = clothing["data-intlkic"]
                imgLink = "https://img.abercrombie.com/is/image/anf/" + imgID + "_prod1?policy=product-medium"

                print(imgLink)

                try:
                    # downloads and vectorizes the image
                    img = download_process_img(imgLink)

                    # add to the dict
                    productDict[productLink] = img

                # sometimes, the image link doesn't work - so we'll just print the link and continue
                except:
                    continue
                    

        
    return productDict


def getTomFord(inputText = "a light green pant"):

    baseMenUrl = "https://www.tomfordfashion.com/men/ready-to-wear/?start=0&sz=500"
    baseWomenUrl = "https://www.tomfordfashion.com/women/ready-to-wear/?start=0&sz=500"
    
    baseURLs = [baseMenUrl, baseWomenUrl]

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

    productDict = {}

    for url in baseURLs:
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, 'lxml')
        clothingContainer = soup.find_all('div', class_="image-container", limit=500)

        for clothing in clothingContainer:
            productLink = "https://www.tomfordfashion.com" + clothing.find('a')["href"]

            imgLink = clothing.find('img')["src"]

            img = download_process_img(imgLink)

            productDict[productLink] = img

    return productDict


if __name__ == "__main__":
    vectorizedText = generate_text_vector("a pink dress")
    print(webScrape(vectorizedText, "Lacoste"))

