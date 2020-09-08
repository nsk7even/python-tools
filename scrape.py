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

def report(type, date, shares, val, newprice):
    if type == "buy":
        print("\t" + date + "       Kauf: %3.2f/%5i € (%3.2f €) " % (shares, val, val/shares),
        "Akt. Wert: %8.2f € " % (newprice * shares),
        "Gewinn: %8.2f € (%2.2f%%)" % (newprice * shares - val, 100/(newprice*shares)*(newprice * shares - val)))
    else:
        newlevel = val / newprice
        newshares = newlevel - shares
        print("\t" + date + "    Verkauf: %3.2f/%5i € (%3.2f €)" % (shares, val, val/shares),
        "n. Ziel: %3.2f St. (-Geb.) " % (newlevel),
        "Entw.: %3.2f St. (%2.2f%%)" % (newshares, 100/shares*newshares))
#        "\n\t> Wiederanlagespiegel: %3.2f Anteile (abzgl. Gebühren) " % (newlevel),
#        "\n\t>         Entwicklung: %3.2f Anteile (%2.2f%%)" % (newshares, 100/shares*newshares))


url = 'https://www.finanzen.net/index/dax-realtime'
points, change = fetch (url, "div", 'col-xs-5', "div", 'col-xs-3')
print("%s %s %s" % ("DAX:".ljust(15), points, change))

url = "https://www.onvista.de/fonds/UNIDEUTSCHLAND-EUR-ACC-Fonds-DE0009750117"
price, change = fetch (url, "span", 'price', "span", 'performance-pct')
print("%s %8.2f EUR %s" % ("UniDeutschland:".ljust(15), price, change))
report("sell", "2020-09-03", 47.790, 10037.81, price)
report("sell", "2020-04-20", 47.149, 8053.84, price)
report("buy", "2020-03-13", 47.149, 7000, price)
report("buy", "2020-02-26", 47.794, 10000, price)

url = "https://www.onvista.de/fonds/UNIRAK-EUR-DIS-Fonds-DE0008491044"
price, change = fetch (url, "span", 'price', "span", 'performance-pct')
print("%s %8.2f EUR %s" % ("UniRak:".ljust(15), price, change))
report("buy", "2018-06-29", 82.432, 10000, price)
report("buy", "2018-02-14", 85.657, 10000, price)


