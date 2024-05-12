import pickle
import image_text_vectorizer as itv

def load_product_list(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

def get_image_vectors_from_products(product_list):
    return {product.image_url: product.image_vector for product in product_list}

def main():
    # Load the vectorized images
    product_list_aritzia = load_product_list('product_list_aritzia.pkl')
    product_list_lacoste = load_product_list('product_list_lacoste.pkl')

    # Combine both product lists into one dictionary
    all_products = {**get_image_vectors_from_products(product_list_aritzia),
                    **get_image_vectors_from_products(product_list_lacoste)}

    # Example GPT-generated text
    gpt_text = "your gpt text here"  # Replace with your actual GPT text

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
