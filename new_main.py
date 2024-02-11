import firebase_admin
from firebase_admin import credentials, firestore, storage
import pickle
import image_text_vectorizer as itv

# Firebase initialization
cred = credentials.Certificate("firebasecredentials.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'shop-d-ea02c.appspot.com'
})

def load_product_list(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

def get_image_vectors_from_products(product_list):
    return {product.image_url: product.image_vector for product in product_list}

def fetch_text_from_firestore():
    db = firestore.client()
    texts = db.collection('userTextInputs').get()
    for text in texts:
        return text.to_dict()['text']

def download_image_from_storage():
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix="uploads/")
    for blob in blobs:
        local_path = f"downloaded_images/{blob.name}"
        blob.download_to_filename(local_path)
        return local_path

def getGPTText(image_path, text_input):
    # Implement your GPT-based processing here
    # This is a placeholder for your actual implementation
    return "Processed GPT text based on image and input text"

def main():
    # Load the vectorized images
    product_list_aritzia = load_product_list('product_list_aritzia.pkl')
    product_list_lacoste = load_product_list('product_list_lacoste.pkl')

    all_products = {**get_image_vectors_from_products(product_list_aritzia),
                    **get_image_vectors_from_products(product_list_lacoste)}

    # Fetch text from Firebase and download the latest image
    text_from_firebase = fetch_text_from_firestore()
    image_from_firebase = download_image_from_storage()

    # Process the fetched text and downloaded image using GPT
    gpt_text = getGPTText(image_from_firebase, text_from_firebase)

    # Convert GPT text to vector
    gpt_text_vector = itv.generate_text_vector(gpt_text).unsqueeze(0)

    # Find closest images
    closest_images = itv.find_closest_images(all_products, gpt_text_vector)

    # Print URLs of closest images
    print("URLs of closest matching images:")
    for image_url, _ in closest_images:
        print(image_url)

if __name__ == "__main__":
    main()
