"""
Craigslist Auto Scraper
Kablam!
"""

import re
import requests
import time
from lxml import html
# from bs4 import BeautifulSoup

class Listing:
    """An individual listing"""
    condition = None
    cylinders = None
    drive = None
    fuel = None
    location = None
    make = None
    odometer = None
    paint_color = None
    size = None
    title_status = None
    transmission = None
    url = None
    vin = None

    def __init__(self, condition, cylinders, drive, fuel, location, make, odometer,
                 paint_color, size, title_status, transmission, url, vin):
        self.condition = condition
        self.cylinders = cylinders
        self.drive = drive
        self.fuel = fuel
        self.location = location
        self.make = make
        self.odometer = odometer
        self.paint_color = paint_color
        self.size = size
        self.title_status = title_status
        self.transmission = transmission
        self.url = url
        self.vin = vin

URLS = []

CITIES = [# "atlanta",
          # "austin",
          # "boston",
          # "chicago",
          "dallas",
          # "denver",
          # "detroit",
          # "houston",
          # "lasvegas",
          # "losangeles",
          # "miami",
          # "newyork",
          # "orangecounty",
          # "philadelphia",
          # "phoenix",
          # "portland",
          # "raleigh",
          # "sacramento",
          # "sandiego",
          # "seattle",
          # "sfbay",
    ]

KEYWORDS = ["minibus",
            "mercedes benz sprinter",
            # "dodge promaster",
            # "ford transit",
            # "nissan nv",
            # "minibus",
]

def generate_start_urls():
    """Generate start URLs"""
    start_urls = []
    for city in CITIES:
        for keyword in KEYWORDS:
            if " " in keyword:
                kws = keyword.split(" ")
                keyword = ""
                for kw in kws:
                    keyword += kw +  "+"
                keyword = keyword[:-1]
            start_urls.append("http://{0}.craigslist.org/search/sss?query={1}".format(city, keyword))
    return start_urls

def generate_individual_list_urls(start_urls):
    """Generate individual list URLs"""
    il_urls = []
    for start_url in start_urls:
        page = requests.get(start_url)
        tree = html.fromstring(page.content)
        il_urls += tree.xpath("//a[@class='result-title hdrlnk']/@href")
    return il_urls

def parse_page(url):
    """Parse page"""
    page = requests.get(url)
    tree = html.fromstring(page.content)
    spans = tree.xpath("//p[@class='attrgroup']/span")

    vin = None
    condition = None
    cylinders = None
    drive = None
    fuel = None
    odometer = None
    paint_color = None
    size = None
    title_status = None
    transmission = None
    make = None

    for span in spans:
        field = span.text
        if field != None:
            field = field.lower()

        value = span.xpath("b/text()")
        if value != []:
            value = value[0]

        # missing location and url
        if field != None:
            if "vin" in field:
                vin = value
            elif "condition" in field:
                condition = value
            elif "cylinders" in field:
                cylinders = value
            elif "drive" in field:
                drive = value
            elif "fuel" in field:
                fuel = value
            elif "odometer" in field:
                odometer = value
            elif "paint color" in field:
                paint_color = value
            elif "size" in field:
                size = value
            elif "title status" in field:
                title_status = value
            elif "transmission" in field:
                transmission = value
            else:
                # If it has a year value, we'll store it as the make
                if re.match(r'[0-9]{4}', field):
                    make = field

    start_index = url.find("//")
    end_index = url.find(".craigs")
    location = url[start_index + 2:end_index]

    print (condition, cylinders, drive, fuel, location, make, odometer,
           paint_color, size, title_status, transmission, url, vin)

    return Listing(condition, cylinders, drive, fuel, location, make, odometer,
                   paint_color, size, title_status, transmission, url, vin)

def run():
    """main"""
    listings = []
    start_urls = generate_start_urls()
    il_urls = generate_individual_list_urls(start_urls)

    for il_url in il_urls:
        time.sleep(.75)
        listings.append(parse_page(il_url))

    # for listing in listings:
    #     print listing


if __name__ == "__main__":
    run()
