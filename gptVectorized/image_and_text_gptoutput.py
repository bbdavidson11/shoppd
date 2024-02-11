import base64
import requests

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def getGPTText(image_from_firebase, text_from_firebase):
    # Encoding the image
    base64_image = encode_image(image_from_firebase)

    # Set up headers for the API call
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Additional text to be added to the payload
    additional_text = "Describe the overall aesthetic of this vision board in two succinct sentences. " + text_from_firebase

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

    # Return the GPT response
    return response.json()


