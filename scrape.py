# scrape.py fetches financial fonds and calculates current values

import sys, requests, json, pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm, tnrange

if len(sys.argv) > 1:
    cfgfile = sys.argv[1]
else:
    print("Usage: " + sys.argv[0] + " <url-of-cfg>")
    sys.exit(1)

def get(url, resulttype):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
        'AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/64.0.3282.167 Safari/537.36'
    }

    result = requests.get(url, headers=headers,verify=True)
    
    if resulttype == "json":
        return json.loads(result.text)
    elif resulttype == "content":
        return result.content
    else:
        return "invalid resulttype!"

def fetch(url, price_el, price_cl, change_el, change_cl):
    htmldata = get(url, "content")
    soup = BeautifulSoup(htmldata, 'html.parser')
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
        print("\t" + date + "       Kauf: %3.2f/%5i € (%6.2f €) " % (shares, val, val/shares),
        "Akt. Wert: %8.2f € " % (newprice * shares),
        "Gewinn: %8.2f € (%6.2f%%)" % (newprice * shares - val, 100/(newprice*shares)*(newprice * shares - val)))
    else:
        newlevel = val / newprice
        newshares = newlevel - shares
        print("\t" + date + "    Verkauf: %3.2f/%5i € (%3.2f €) " % (shares, val, val/shares),
        "Neukauflevel (-Geb.): %3.2f St. " % (newlevel),
        "Entw.: %5.2f St. (%6.2f%%)" % (newshares, 100/shares*newshares))
#        "\n\t> Wiederanlagespiegel: %3.2f Anteile (abzgl. Gebühren) " % (newlevel),
#        "\n\t>         Entwicklung: %3.2f Anteile (%2.2f%%)" % (newshares, 100/shares*newshares))

# CONFIG
cfg = get(cfgfile, "json")
#print(cfg)

# DAX
url = 'https://www.finanzen.net/index/dax-realtime'
points, change = fetch (url, "div", 'col-xs-5', "div", 'col-xs-3')
print("%s %s %s" % ("DAX:".ljust(15), points, change))

# UniDeutschland
url = "https://www.onvista.de/fonds/UNIDEUTSCHLAND-EUR-ACC-Fonds-DE0009750117"
price, change = fetch (url, "span", 'price', "span", 'performance-pct')
print("%s %8.2f EUR %s" % ("UniDeutschland:".ljust(15), price, change))

for datekey in cfg["UniDeutschland"]:
    op = cfg["UniDeutschland"][datekey]
    report(op["type"], datekey, float(op["shares"]), float(op["value"]), price)

# UniRak
url = "https://www.onvista.de/fonds/UNIRAK-EUR-DIS-Fonds-DE0008491044"
price, change = fetch (url, "span", 'price', "span", 'performance-pct')
print("%s %8.2f EUR %s" % ("UniRak:".ljust(15), price, change))

for datekey in cfg["UniRak"]:
    op = cfg["UniRak"][datekey]
    report(op["type"], datekey, float(op["shares"]), float(op["value"]), price)


