import os
import pandas as pd
import image_text_vectorizer as itv
import pickle

class Product:
    def __init__(self, image_url, image_vector):
        self.image_url = image_url
        self.image_vector = image_vector

def load_image_urls(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    return df[0].tolist()

def get_image_vectors(folder_path):
    image_vectors = []
    if os.path.exists(folder_path):
        sorted_filenames = sorted(os.listdir(folder_path))
        for filename in sorted_filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    image_vector = itv.generate_vector(file_path)
                    image_vectors.append(image_vector)
    else:
        raise FileNotFoundError(f"Error: Image folder '{folder_path}' does not exist")
    return image_vectors

def create_product_list(image_urls, image_vectors):
    if len(image_urls) != len(image_vectors):
        raise ValueError("Warning: The number of URLs does not match the number of images")

    return [Product(url, vector) for url, vector in zip(image_urls, image_vectors)]

def save_product_list(product_list, filename):
    with open(filename, 'wb') as file:
        pickle.dump(product_list, file)
    print(f'Product list has been successfully pickled to {filename}')

def main():
    # Aritzia
    image_urls_aritzia = load_image_urls('image_url.xlsx', '1')
    image_vectors_aritzia = get_image_vectors('screenshots_aritzia')
    product_list_aritzia = create_product_list(image_urls_aritzia, image_vectors_aritzia)
    save_product_list(product_list_aritzia, 'product_list_aritzia.pkl')

    # Lacoste
    image_urls_lacoste = load_image_urls('image_url.xlsx', '2')
    image_vectors_lacoste = get_image_vectors('screenshots_lacoste')
    product_list_lacoste = create_product_list(image_urls_lacoste, image_vectors_lacoste)
    save_product_list(product_list_lacoste, 'product_list_lacoste.pkl')

if __name__ == "__main__":
    main()
