import requests
from bs4 import BeautifulSoup  
import pandas as pd
from tqdm import tqdm, tnrange

url = 'https://www.finanzen.net/index/dax-realtime'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
    'AppleWebKit/537.36 (KHTML, like Gecko)'
    'Chrome/64.0.3282.167 Safari/537.36'
}
result = requests.get(url, headers=headers,verify=True)
#print(result)

soup = BeautifulSoup(result.content, 'html.parser')
price = soup.find("div", class_='col-xs-5').getText().strip()
change = soup.find("div", class_='col-xs-3').getText().strip()

print("DAX: " + price + " " + change)

url = "https://www.onvista.de/fonds/UNIDEUTSCHLAND-EUR-ACC-Fonds-DE0009750117"
result = requests.get(url, headers=headers,verify=True)
#print(result)

soup = BeautifulSoup(result.content, 'html.parser')
price = soup.find("span", class_='price').getText().strip()
change = soup.find("span", class_='performance-pct').getText().strip()

print("UniDeutschland: " + price + " " + change)

unid = float(price.replace("EUR", "").replace(",", ".").strip())

print("\t2020-03-13  Anlage:  7000  Akt. Wert: %8.2f EUR  Gewinn: %8.2f EUR" % (unid * 47.149, unid * 47.149 - 7000))
print("\t2020-02-26  Anlage: 10000  Akt. Wert: %8.2f EUR  Gewinn: %8.2f EUR" % (unid * 47.794, unid * 47.794 - 10000))

url = "https://www.onvista.de/fonds/UNIRAK-EUR-DIS-Fonds-DE0008491044"
result = requests.get(url, headers=headers,verify=True)
#print(result)

soup = BeautifulSoup(result.content, 'html.parser')
price = soup.find("span", class_='price').getText().strip()
change = soup.find("span", class_='performance-pct').getText().strip()

print("UniRak: " + price + " " + change)

unir = float(price.replace("EUR", "").replace(",", ".").strip())

print("\t2018-06-29  Anlage: 10000  Akt. Wert: %8.2f EUR  Gewinn: %8.2f EUR" % (unir * 82.432, unir * 82.432 - 10000))
print("\t2018-02-14  Anlage: 10000  Akt. Wert: %8.2f EUR  Gewinn: %8.2f EUR" % (unir * 85.657, unir * 85.657 - 10000))

