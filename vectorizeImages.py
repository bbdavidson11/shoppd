import os
import pandas as pd
import image_text_vectorizer as itv
import pickle

class Product:
    def __init__(self, image_url, image_vector):
        self.image_url = image_url
        self.image_vector = image_vector

df = pd.read_excel('screenshotVectors.xlsx', header=None)
image_urls = df[0].tolist()

folder_path = 'screenshotsV'

image_vectors = []
product_list = []

if os.path.exists(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                image_vector = itv.generate_vector(file_path)
                image_vectors.append(image_vector)
else:
    print("Error: Image folder 'screenshotsV' does not exist")

# Check if the number of URLs matches the number of images
if len(image_urls) != len(image_vectors):
    print("Warning: The number of URLs does not match the number of images")

for url, vector in zip(image_urls, image_vectors):
    product = Product(url, vector)
    product_list.append(product)

pickle_filename = 'product_list.pkl'

with open(pickle_filename, 'wb') as file:
    pickle.dump(product_list, file)

print(f'Product list has been successfully pickled to {pickle_filename}')
