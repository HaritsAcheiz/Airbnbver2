import requests
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import os
from datetime import date, timedelta
import json

@dataclass
class Scraper:

    def generate_url(self, places):
        checkin = date.today() + timedelta(days=7)
        checkout = checkin + timedelta(days=1)
        urls = [f"https://www.airbnb.com/s/{place}/homes?adults=1&checkin={checkin}&checkout={checkout}" for place in places]
        return urls

    def fetch(self, url):
        with requests.Session() as s:
            r = s.get(url)
        print(r)
        return r.text

    def parse(self, html):
        tree = HTMLParser(html)
        json_data = json.loads(tree.css_first('script#data-state').text())
        json_formatted_str = json.dumps(json_data, indent=2)
        print(json_formatted_str)
        items = []
        i = 0
        while 1:
            try:
                name = json_data['model']['inAreaResultViews'][i]['name']
                address = json_data['model']['inAreaResultViews'][i]['primaryAddress']
                phone = json_data['model']['inAreaResultViews'][i]['callContactNumber']['value']
                email = json_data['model']['inAreaResultViews'][i]['primaryEmail']
                website = json_data['model']['inAreaResultViews'][i]['website']
                detail = json_data['model']['inAreaResultViews'][i]['detailsLink']
                items.append(asdict(
                    Company(name=name, address=address, phone=phone, email=email, website=website, detail=detail)))
                i += 1
            except Exception as e:
                print(e)
                break
        return items

if __name__ == '__main__':
    s = Scraper()
    urls = s.generate_url(['New-Zealand'])
    htmls = [s.fetch(url) for url in urls]
    data = s.parse(htmls[0])