# Shopp'd
Shopp'd is a simple website that aims to help you find the clothes you want! 

Simply upload an image containing the clothing you're looking for, describe the article of clothing you want from the image - and we'll do the rest. Our current website is capable of live-webscraping select stores in order to find the best match for you.

Future Updates will include the following:
- Include "About Us", "Vision", and "Join Waitlist" pages

# How to Run
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
4. Create a Firebase Account and create a new Firestore Project
5. Grab your Firestore Credentials, rename the file to ServiceAccountKey.json, and move it into the project. References on how to do this found [here](https://www.youtube.com/watch?v=yylnC3dr_no&t=321s)
6. Run application.py
7. Run *home.html* located in */website/home.html

Note: If the last web-scrape of the chosen store was over a week ago, then the app will automatically initiate a web-scrape. This scrape might cause response times to increase significantly (up to 10 minutes for a full scrape based on current parameters)

