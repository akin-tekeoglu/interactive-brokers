import argparse
from pypdf import PdfReader
import datetime
import os
import re


parser = argparse.ArgumentParser()
parser.add_argument("--forecast")
args = parser.parse_args()
forecast=int(args.forecast)
text=None
while True:
    os.system('curl -o jobless_claims.pdf "https://www.dol.gov/ui/data.pdf"')
    reader = PdfReader("jobless_claims.pdf")
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    today=datetime.datetime.now().date()
    month=today.strftime("%B")
    day=today.day
    if "{month} {day}" in text:
        break

result = re.findall("initial claims  was (.*), ", text)
change=int(str(result[0]).replace(",",""))
diff=change-forecast
ratio=abs(diff/forecast)
if diff>0 or diff==0:
    print(f"BUY {ratio}")
else:
    print(f"SELL {1/ratio}")
    
