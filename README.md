# Shopp'd
Shopp'd is a simple website that aims to help you find the clothes you want! 

Simply upload an image containing the clothing you're looking for, describe the article of clothing you want from the image - and we'll do the rest.

Future Updates will include the following:
- Live Webscraping
- Option to explore clothing from more sites
- Include "About Us", "Vision", and "Join Waitlist" pages


# How to Run
Unfortunately, we currently don't have an active website at this moment.

If you would like to run this app locally, just do the following:

1. Clone the repo to your local machine
2. Download the required packages. The following is non-comprehensive and may be subjected to change:

```
pip install firebase firebase_admin numpy pandas flask-cors flask pillow torch requests beautifulsoup4 git+https://github.com/openai/CLIP.git
```
3. Create a *.env* file and add a GPT API Key with the variable name 'gptAPI':

``` 
gptAPI = "sk-proj-abcdefghijklmonpXXXXXXXXXX"
```
4. Run application.py
5. Run *home.html* located in */website/home.html

Note: At this moment, only the Aritzia option works, and all links and images are stored locally rather than web scraped 

