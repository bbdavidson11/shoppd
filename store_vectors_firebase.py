import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def storeTo(path, info):
    print("nothing")

if __name__ == "__main__":

    testInfo = [('https://www.tomfordfashion.com/shiny-fringe-cocktail-dress/AB3355-FAE403.html', 0.24585619568824768), 
                ('https://www.tomfordfashion.com/open-back-knit-evening-dress/ACK414-YAX619.html', 0.23224158585071564), 
                ('https://www.tomfordfashion.com/openwork-lurex-scoop-neck-maxi-dress/ACK416-YAX648.html', 0.2241399884223938), 
                ('https://www.tomfordfashion.com/soft-suede-jean-jacket/LBS042-LMS005S23.html', 0.21322093904018402), 
                ('https://www.tomfordfashion.com/sable-halter-neck-belted-jumpsuit/TU0269-FAX1105.html', 0.21301044523715973), 
                ('https://www.tomfordfashion.com/open-back-knit-evening-dress/ACK460-YAX704.html', 0.21056944131851196), 
                ('https://www.tomfordfashion.com/soft-suede-contrast-4-zip-western/LBS037-LMS005S23.html', 0.14060480892658234), 
                ('https://www.tomfordfashion.com/grain-leather-jean-jacket/LBS038-LMG014S24.html', 0.13118800520896912), 
                ('https://www.tomfordfashion.com/shiny-feather-nappa-zip-racer-jacket/LXR014-LMN009F23.html', 0.11114542186260223), 
                ('https://www.tomfordfashion.com/soft-suede-pilot-bomber/LBS033-LMS005S23.html', 0.10456178337335587)]
    storeTo("testStoring", testInfo)
