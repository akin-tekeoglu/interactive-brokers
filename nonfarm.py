import argparse
import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--forecast")
args = parser.parse_args()
forecast=int(args.forecast)
root=None
while True:
    response=requests.get("https://www.bls.gov/feed/ces_latest.rss")
    root = ElementTree.fromstring(response.content)
    date=root.find("./channel/item/pubDate")
    parsed_date=datetime.datetime.strptime(date.text, '%a,  %d %b %Y %H:%M:%S %z')
    if parsed_date.date() == datetime.datetime.today().date():
        break

description=root.find("./channel/item/description")
soup = BeautifulSoup(description.text, 'html.parser')
nonfarm=soup.find("strong")
change=int(nonfarm.text.split("(p)")[0].replace(",",""))
diff=change-forecast
ratio=abs(diff/forecast)
if diff>0 or diff==0:
    print(f"SELL {ratio}")
else:
    print(f"BUY {1/ratio}")
