from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
from PIL import Image
import requests

def get_webpage_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        result = page.content()
        browser.close()
    return result


#MAIN
linkList=[]
with open('player.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        linkList.append(row[-1])

linkList.pop(0)
print (linkList)
#Put data in csv
with open("Img.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(linkList)
# recupération du html
cpt=0
for link in linkList:
    page_content = get_webpage_content(link)
    # BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    image = soup.find('img',attrs={'class','PlayerImage_image__1smob w-10/12 mx-auto mt-16 md:mt-24'})
    image_url = image['src']
    print(image_url)
    r = requests.get(image_url)
    file = open("Player_Img\image"+str(cpt)+".png", "wb")
    file.write(r.content)
    file.close()
    cpt+=1

