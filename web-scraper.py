import requests
from bs4 import BeautifulSoup
import lxml

if __name__ == "__main__":
    url = "https://www.aritzia.com/us/en/clothing?lastViewed=300"
    html = requests.get(url)

    soup = BeautifulSoup(html.content, 'lxml')