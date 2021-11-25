#installation de playwright qui remplace requests
#playwright install

#IMPORT
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv

#FONCTION POUR SCRAP
#Contenue de la page :
def get_webpage_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        result = page.content()
        browser.close()
    return result

#Table :
def get_table_head_fields_as_list(table_obj):
    result = []
    table_head = table_obj.find('thead')
    table_head_fields = table_head.find_all('th')
    for field_obj in table_head_fields:
        result.append(field_obj.getText().strip())
    return result

def get_table_body_as_lists(table_obj):
    result = []
    table_body = table_obj.find('tbody')
    table_rows = table_body.find_all('tr')
    for row in table_rows:
        curr_row = []
        row_fields = row.find_all('td')
        for field_obj in row_fields:
            curr_row.append(field_obj.getText().strip())
        result.append(curr_row)
    return result

def get_link_player(table_obj):
    result=[]
    table_body = table_obj.find('tbody')
    table_rows = table_body.find_all('tr')
    for row in table_rows:
        curr_row = []
        row_fields = row.find_all('td',attrs={'class':'player'})
        for field_obj in row_fields:
            curr_row.append('https://www.nba.com/'+ field_obj.a['href'])
        result.append(curr_row)
    return result

#MAIN
url = 'https://www.nba.com/stats/leaders/'

# recupération du html
page_content = get_webpage_content(url)

# BeautifulSoup
soup = BeautifulSoup(page_content, 'html.parser')

#Recuperer la table
table = soup.find('table')
#récupération des données
table_head = get_table_head_fields_as_list(table)
table_body = get_table_body_as_lists(table)
table_link= get_link_player(table)


# Tableau final
final_table_data = [table_head] + table_body
for i in range (0, len(table_link)+1):
    if i==0 :
        final_table_data[0].append('LINK TO PLAYER PAGE')
    else:
        final_table_data[i].append(str(table_link[i-1]).strip('[]').strip('\'\''))

# Print the data
for row in final_table_data:
    print(row)

#Put data in csv
with open("player.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(final_table_data)

