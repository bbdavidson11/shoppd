import firebase_admin
from firebase_admin import credentials, firestore, storage
import pickle
import image_text_vectorizer as itv
import sys
import base64
from PIL import Image
from io import BytesIO
sys.path.append('gptVectorized')
from gptVectorized.image_and_text_gptoutput import getGPTText
from scraper_and_comparer import webScrape

class Product:
    def __init__(self, image_url, image_vector):
        self.image_url = image_url
        self.image_vector = image_vector

# Firebase initialization
cred = credentials.Certificate("firebasecred.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'shop-d-ea02c.appspot.com'
})

def load_product_list(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

def get_image_vectors_from_products(product_list):
    return {product.image_url: product.image_vector for product in product_list}

def fetch_text_from_firestore(userPath):
    db = firestore.client()
    text = db.collection('userTextInputs').document(userPath).get()

    # we're basically retrieving the user's input text which should be the value under "text"
    # if we don't get anything, we'll just return "" which we're assuming the user just skipped this step
    if text.exists:
        data = text.to_dict()
        key = "text"
        if key in data:
            return data[key]
        else:
            return ""
    else:
        return ""

def download_image_from_storage(userPath):
    bucket = storage.bucket()
    firebasePath = "uploads/" + userPath 
    blobs = bucket.list_blobs(prefix=firebasePath)


    for blob in blobs:
        # Check if blob is folder - then skip if it is
        if blob.name.endswith("/"):
             continue

        # Download image as bytes
        image_bytes = blob.download_as_string()

        # Convert bytes to Pillow image
        image = Image.open(BytesIO(image_bytes))

        return image_to_base64(image)
    
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")  # Convert the image to PNG format and save to the buffer
    encoded_image = base64.b64encode(buffered.getvalue())  # Encode the image buffer to base64
    return encoded_image.decode('utf-8')  # Convert bytes to string and return

def main(userPath):

    # for testing purposes
    data = { 
            "status" : "success",
            "message" : "main.py executed",
        }

    # Load the vectorized images
    product_list_aritzia = load_product_list('product_list_aritzia.pkl')

    all_products = get_image_vectors_from_products(product_list_aritzia)

    # Fetch text from Firebase and download the latest image
    text_from_firebase = fetch_text_from_firestore(userPath)
    print(text_from_firebase)

    image_from_firebase = download_image_from_storage(userPath)
    # image_from_firebase = "downloaded_images/currImage.webp" <----- use to debug if you want to test everything but downlaoding from firebase
    #                                                                   make sure that the folder and image exists for this to work.

    # Process the fetched text and downloaded image using GPT
    gpt_text = getGPTText(image_from_firebase, text_from_firebase)
    print("FROM GPT: " + gpt_text)

    # Convert GPT text to vector
    gpt_text_vector = itv.generate_text_vector(gpt_text)

    # Find closest images
    closest_images = itv.find_closest_images(all_products, gpt_text_vector)

    topMatches = {}

    # might be useless code, probably only have to return closest_images tbh
    for image_url, similarityScore in closest_images:
        #  print(str(similarityScore) + " " + str(image_url)) <----- use to debug
         topMatches['url' + str(x)] = image_url
         x+=1

    # use to debug vvvvvv
    print(topMatches)

    return topMatches

if __name__ == "__main__":
    main('testfolder')
