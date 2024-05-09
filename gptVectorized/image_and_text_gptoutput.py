import requests
import os
from dotenv import load_dotenv

# OpenAI API Key
load_dotenv()
api_key = os.environ['gptAPI']

# Function to encode the image
# haven't added code to debug yet
def encode_image(image_path, debug=False):
    # I changed the function so that image is already in encoded in base64 - too lazy to refactor this tho
    return image_path

def getGPTText(image_from_firebase, text_from_firebase):
    # Encoding the image
    base64_image = encode_image(image_from_firebase)

    # Set up headers for the API call
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Additional text to be added to the payload
    additional_text = "In exactly 2 sentences and less than 100 characters, describe the specific clothing (singular) as if you were describing it to a shop keeper: " + text_from_firebase

    # Construct the payload
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": additional_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    # Make the API request
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print("GPT RESPONSE: \n" + str(response))

    response = response.json()

    # Return the GPT response
    return response['choices'][0]['message']['content']


