import requests
from bs4 import BeautifulSoup
import pandas as pd
import json 
from geopy.geocoders import Nominatim
from datetime import datetime
from airflow.hooks.S3_hook import S3Hook


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
            'Images':"https://" + tds[5].find('img').get('src').split("//")[1] if tds[5].find('img') else "NO_IMAGE",
            'Home_team':clean_text(tds[6].text)
        }
        data.append(values)

    json_data = json.dumps(data)
    kwargs['ti'].xcom_push(key="rows",value=json_data)
    
    return "Done"

def get_lat_long(country,city):
    geolocator = Nominatim(user_agent="geoapiExercises")

    location = geolocator.geocode(f'{city},{country}')

    if location:
        return location.latitude,location.longitude

    return None


def transform_data(**kwargs):
    data = kwargs['ti'].xcom_pull(key="rows",task_ids="extract_data")

    data = json.loads(data)

    stadium_df = pd.DataFrame(data).replace(['NO_IMAGE',"",None],NO_IMAGE)
    
    # stadium_df['location'] = stadium_df.apply(lambda x: get_lat_long(x['Country'],x['Stadium']),axis=1)
    

    # duplicates = stadium_df[stadium_df.duplicated['location']]
    # duplicates['location'] = duplicates.apply(lambda x:get_lat_long(x['Country',x['City']]),axis=1)
    # stadium_df.update(duplicates)

    # stadium_df.to_csv("output")

    kwargs['ti'].xcom_push(key='rows',value=stadium_df.to_json())

    return "OK"

def writing_data(**kwargs):
    data = kwargs['ti'].xcom_pull(key='rows',task_ids="transform_data")

    data = json.loads(data)
    df = pd.DataFrame(data)
    file_path = f'footbal_stadium_data_{str(datetime.now().date())}.csv'
    bucket_name = 'football-s3-aman'
    folder_name = 'landing'

    df.to_csv(
        f"s3://{bucket_name}/{folder_name}/{file_path}",
        storage_options={
        "key": 'ASIAQEIP3OY7UVU6MLSL',
        "secret": 'MkhBssMRmRg8Y5MLqOU8EQydIuGX6KWwCuFm5Fvf',
       
        },
        index=False)




    