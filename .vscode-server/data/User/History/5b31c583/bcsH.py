import requests
from bs4 import BeautifulSoup
import pandas as pd
import json 
from geopy.geocoders import Nominatim
import time


NO_IMAGE = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.reformsports.com%2Fwhat-are-the-three-types-of-stadium%2F&psig=AOvVaw22Cs1C0_OJivdUTujYyKi9&ust=1731751251505000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCJDzgqSK3okDFQAAAAAdAAAAABAE"
def get_page(url):
    try:
        response = requests.get(url)
        print(response)
        return response.text
    except Exception as e:
        return e
    
def getData(html):
    soup = BeautifulSoup(html,'html.parser')
    tables = soup.find_all('table',{"class":"wikitable"})[1]
    table_rows = tables.find_all('tr')

    return table_rows

def clean_text(text):
    text = str(text).strip()

    text = text.replace(' â™¦',"")

    if text.find('[') != -1:
        text = text.split('[')[0]
    
    if text.find(' ♦'):
        text = text.split(' ♦')[0]

    return text.replace('\n',"")

def main_extract_data(**kwargs):
    url = kwargs.get('url')
    html = get_page(url)
    rows = getData(html)

    # print("print ROWS --",rows)
    data=[]
    for i in range(1,len(rows)):
        tds = rows[i].find_all('td')
        values ={
            'Rank':i,
            'Stadium':clean_text(tds[0].text),
            'Seating Capacity':clean_text(tds[1].text).replace(',',""),
            'Region':clean_text(tds[2].text),
            'Country':clean_text(tds[3].text),
            'City':clean_text(tds[4].text),
            'Images':"https://" + tds[5].find('img').get('src').split("//")[1] if tds[5].find('img') else "No Image",
            'Home_team':clean_text(tds[6].text)
        }
        data.append(values)

    json_data = json.dumps(data)
    kwargs['ti'].xcom_push(key="rows",value=json_data)
    
    return "Done"

def get_lat_long(country, city, retries=3):
    geolocator = Nominatim(user_agent="my_app")
    for attempt in range(retries):
        try:
            location = geolocator.geocode(f"{country}, {city}")
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # Retry after 1 second
    return None, None


def transform_data(**kwargs):
    data = kwargs['ti'].xcom_pull(key="rows",task_ids="extract_data")

    data = json.loads(data)

    stadium_df = pd.DataFrame(data).replace(['NO_IMAGE',"",None],NO_IMAGE)
    
    stadium_df['location'] = stadium_df.apply(lambda x: get_lat_long(x['Country'],x['Stadium']),axis=1)
    

    duplicates = stadium_df.duplicated['location']
    duplicates['location'] = duplicates.apply(lambda x:get_lat_long(x['Country',x['City']]),axis=1)
    stadium_df.update(duplicates)

    stadium_df.to_csv("output")

    # kwargs['ti'].xcom_push(key='rows',value=stadium_df.to_json())

    # return "OK"



    