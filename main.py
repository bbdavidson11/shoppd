import firebase_admin
from firebase_admin import credentials, firestore, storage
import pickle
import image_text_vectorizer as itv
import sys
import os
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
sys.path.append('gptVectorized')
from gptVectorized.image_and_text_gptoutput import getGPTText

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

    blob = bucket.blob(firebasePath)

    # checks if folder exists
    # we'll download the image here if needed to (you will have to uncomment some items below)
    if not os.path.exists("downloaded_images"):
        os.makedirs("downloaded_images")

    # myImage = bucket.get_blob(firebasePath)
    # downloadUrl = blob.generate_signed_url(10000)

    # blob.download_to_filename("downloaded_images/currImage2.webp")
    # print(downloadUrl)

    # blob.download_to_file

    for blob in blobs:
        # Check if blob is folder - then skip if it is
        if blob.name.endswith("/"):
             continue

        # uncomment to view the image as a pop-up
        # cv2.imshow('image', img)
        # cv2.waitKey(0)

        # parsed path to get name + extension of file iif needed
        downloadName = os.path.join("downloaded_images", blob.name.split("/")[2])
        extension = blob.name.split("/")[2].split('.')[1]

        print("extension: " + extension)

        if extension == "webp":
            image_bytes = blob.download_as_string()

            # Load the WebP image using Pillow
            image = Image.open(BytesIO(image_bytes))

            # Convert the image to RGB format if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Save the image to a byte buffer in WebP format
            buffer = BytesIO()
            image.save(buffer, format='WebP')
            buffer.seek(0)
            return buffer

        else:
            # download image as array of bytes
            arr = np.frombuffer(blob.download_as_string(), np.uint8)
            img = cv2.imdecode(arr, cv2.COLOR_BGR2BGR555) #gets the image
            _, buffer = cv2.imencode(extension, img)     # Convert the image to a byte buffer
            return buffer

def main(userPath):

    # for testing purposes
    data = { 
            "status" : "success",
            "message" : "main.py executed",
        }

    # Load the vectorized images
    product_list_aritzia = load_product_list('product_list_aritzia.pkl')
    # product_list_lacoste = load_product_list('product_list_lacoste.pkl')

    # all_products = {**get_image_vectors_from_products(product_list_aritzia),
    #                 **get_image_vectors_from_products(product_list_lacoste)}

    all_products = get_image_vectors_from_products(product_list_aritzia)

    # Fetch text from Firebase and download the latest image
    text_from_firebase = fetch_text_from_firestore(userPath)
    print(text_from_firebase)

    image_from_firebase = download_image_from_storage(userPath)
    # image_from_firebase = "downloaded_images/currImage.webp"

    # Process the fetched text and downloaded image using GPT
    gpt_text = getGPTText(image_from_firebase, text_from_firebase)
    print("FROM GPT: " + gpt_text)

    # Convert GPT text to vector
    gpt_text_vector = itv.generate_text_vector(gpt_text)

    # Find closest images
    closest_images = itv.find_closest_images(all_products, gpt_text_vector)

    # Save URLs of closest images to Firestore
    # db = firestore.client()
    # urls_collection = db.collection('matchedImageUrls')

    # x = 1
    # for image_url, _ in closest_images:
    #     urlName = 'url' + str(x)
    #     urls_collection.add({urlName: image_url})
    #     print(image_url)

    topMatches = {}

    x = 1
    for image_url, similarityScore in closest_images:
        #  print(str(similarityScore) + " " + str(image_url))
         topMatches['url' + str(x)] = image_url
         x+=1

    # finalResults = json.dumps(topMatches)

    return topMatches

if __name__ == "__main__":
    main('testfolder')
