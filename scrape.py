import requests
from bs4 import BeautifulSoup  
import pandas as pd
from tqdm import tqdm, tnrange

def fetch(url, price_el, price_cl, change_el, change_cl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
        'AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/64.0.3282.167 Safari/537.36'
    }

    result = requests.get(url, headers=headers,verify=True)
    #print(result)

    soup = BeautifulSoup(result.content, 'html.parser')
    course = soup.find(price_el, class_=price_cl).getText().strip()
    change = soup.find(change_el, class_=change_cl).getText().strip()
    
    course = xtract(course)
    
    return course, change

def xtract(input):
    if type(input) is not str:
        return input
    if "EUR" in input:
        return float(input.replace("EUR", "").replace(",", ".").strip())
    else:
        return input

def report(date, shares, val, newprice):
    print("\t" + date + "  Anlage:  %5i  Akt. Wert: %8.2f EUR  Gewinn: %8.2f EUR" % (val, newprice * shares, newprice * shares - val))


url = 'https://www.finanzen.net/index/dax-realtime'
points, change = fetch (url, "div", 'col-xs-5', "div", 'col-xs-3')
print("%s %s %s" % ("DAX:".ljust(15), points, change))

url = "https://www.onvista.de/fonds/UNIDEUTSCHLAND-EUR-ACC-Fonds-DE0009750117"
price, change = fetch (url, "span", 'price', "span", 'performance-pct')
print("%s %8.2f EUR %s" % ("UniDeutschland:".ljust(15), price, change))
report("2020-03-13", 47.149, 7000, price)
report("2020-02-26", 47.794, 10000, price)

url = "https://www.onvista.de/fonds/UNIRAK-EUR-DIS-Fonds-DE0008491044"
price, change = fetch (url, "span", 'price', "span", 'performance-pct')
print("%s %8.2f EUR %s" % ("UniRak:".ljust(15), price, change))
report("2018-06-29", 82.432, 10000, price)
report("2018-02-14", 85.657, 10000, price)


