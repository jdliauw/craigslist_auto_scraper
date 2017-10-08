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
    list_price = None
    location = None
    make = None
    odometer = None
    paint_color = None
    size = None
    title_status = None
    transmission = None
    url = None
    vin = None

    def __init__(self, condition, cylinders, drive, fuel, list_price, location, make,
                 odometer, paint_color, size, title_status, transmission, url, vin):
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

"""
    MULTIPLE (just add again)

    condition: &condition=
    10=new, 20=like new, 30=excellent, 40=good, 50=fair, 60=salvage

    cylinders: &auto_cylinders=
    1=3,2=4,3=5,4=6,5=8,6=10,7=12

    drive: &auto_drivetrain=
    1=fwd,2=rwd,3=4wd 

    fuel: &auto_fuel_type=
    1=gas,2=diesel,3=hybrid,4=electric,5=other

    color: &auto_paint=
    1=black,2=blue,20=brown,3=green,4=grey,5=orange,6=purple,7=red,8=silver,9=white,10=yellow,11=custom

    size: &auto_size=1
    1=compact,2=full-size,3=mid-size,4=sub-compact

    title_status: &auto_title_status=
    1=clean,2=salvage,3=rebuilt,4=parts only,5=lien,6=missing

    transmission: &auto_transmission=
    1=manual,2=automatic,3=other

    type: &auto_bodytype=
    1=bus,2=convertible,3=coupe,4=hatchback,5=mini-van,6=offroad,7=pickup,8=sedan,9=truck,10=SUV,11=wagon,12=van,13=other

"""

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

    # return string instead of list and remove $
    list_price = tree.xpath("//span[@class='price']/text()")[0][1:]
    if list_price is None:
        return None

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

    print (condition, cylinders, drive, fuel, list_price, location, make,
           odometer, paint_color, size, title_status, transmission, url, vin)

    return Listing(condition, cylinders, drive, fuel, list_price, location, make, odometer,
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
