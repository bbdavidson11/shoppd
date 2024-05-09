import torch
import clip
# note, install clip using the following: 'pip install git+https://github.com/openai/CLIP.git'
from PIL import Image
import os
import numpy as np

# Load the CLIP model
model, preprocess = clip.load("ViT-B/32")

# Function to generate vector from an image
def generate_vector(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0)
    with torch.no_grad():
        image_features = model.encode_image(image)
    return image_features

# Function to generate a vector from text
def generate_text_vector(text):
    with torch.no_grad():
        text_features = model.encode_text(clip.tokenize(text))
        # print("Shape of Text Vector from generated text:", text_features.shape)
    return text_features

# Function to process all images in the directory and return their vectors
def process_directory(directory_path):
    image_vectors = {}
    for image_name in os.listdir(directory_path):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            image_path = os.path.join(directory_path, image_name)
            image_vectors[image_name] = generate_vector(image_path)
    return image_vectors

# Function to find the closest images to the text
def find_closest_images(image_vectors, text_vector, n=10):
    print("Shape of text vector:", text_vector.shape)
    # print("Shape of image vector:", image_vectors.shape)
    # Calculate cosine similarity
    similarities = {image_name: torch.nn.functional.cosine_similarity(text_vector, image_vector).item()
                    for image_name, image_vector in image_vectors.items()}
    
    # Sort images by highest similarity
    closest_images = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
    return closest_images[:n]

# Example usage
if __name__ == "__main__":
    directory_path = "F:\Shoppd Project\shoppd\screenshots_aritzia"  # Replace with your image directory
    vectors = process_directory(directory_path)

    print(vectors)
    
    # Example text input
    sample_text = "green pair of pants"  # Replace with your text input
    text_vector = generate_text_vector(sample_text)
    
    # Find and print the 5 most similar images to the text input
    closest_images = find_closest_images(vectors, text_vector)
    print("Top matches for the input text:")
    for image_name, similarity in closest_images:
        print(f"{image_name}: {similarity}")