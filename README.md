# Shopp'd
Shopp'd is a simple website that aims to help you find the clothes you want! 

Simply upload an image containing the clothing you're looking for, describe the article of clothing you want from the image - and we'll do the rest. Our current website is capable of live-webscraping a number of stores in order to find the best match for you.

Future Updates will include the following:
- Storing Livescraped data to Firestore to allow shorter wait times
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
4. Create a Firebase Account and create a new Firestore Project
5. Grab your Firestore Credentials, rename the file to ServiceAccountKey.json, and move it into the project. References on how to do this found [here](https://www.youtube.com/watch?v=yylnC3dr_no&t=321s)
6. Run application.py
7. Run *home.html* located in */website/home.html

Note: At this moment, only the Aritzia option works, and all links and images are stored locally rather than web scraped 

