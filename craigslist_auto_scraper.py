"""
Craigslist Auto Scraper
Kablam!
"""

import json
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

def query_string_creation(parameters):
    """
    craiglists query string filters are in the format: "&<field>=<value>""
    For example: &condition=10 represents a new condition
    Multiple conditions and fields can be chosen, and are just appended in the same format
    """

    query_string = ""
    conditions    = {"new":10, "like new":20, "excellent":30, "good":40, "fair":50, "salvage":60}
    cylinders     = {3:1, 4:2, 5:3, 6:4, 8:5, 10:6, 12:7}
    drives        = {"fwd":1, "rwd":2, "4wd":3}
    fuels         = {"gas":1, "diesel":2, "hybrid":3, "electric":4} # "other":5
    colors        = {"black":1, "blue":2, "brown":20, "green":3, "grey":4, "orange":5, "purple":6,
                     "red":7, "silver":8, "white":9, "yellow":10, "custom":11}
    sizes         = {"compact":1, "full-size":2, "mid-size":3, "sub-compact":4}
    titles        = {"clean":1, "salvage":2, "rebuilt":3, "parts only":4, "lien":5, "missing":6}
    transmissions = {"manual":1, "automatic":2} # "other":3
    types         = {"bus":1, "convertible":2, "coupe":3, "hatchback":4, "mini-van":5, "offroad":6,
                     "pickup":7, "sedan":8, "truck":9, "SUV":10, "wagon":11, "van":12, "other":13}

    # dictionary not hashable, so reversed so string:dict
    fields = {"&condition=":conditions,
              "&auto_cylinders=":cylinders,
              "&auto_drivetrain=":drives,
              "&auto_fuel_type=":fuels,
              "&auto_paint=":colors,
              "&auto_size=":sizes,
              "&auto_title_status=":titles,
              "&auto_transmission=":transmissions,
              "&auto_bodytype=":types,
              }

    for field in fields:
        for field_value in fields[field]:
            if str(field_value) in parameters:
                query_string += "{0}{1}".format(field, fields[field][field_value])
    return query_string

def generate_start_urls(cities, keywords, parameters):
    """Generate start URLs"""
    start_urls = []

    for city in cities:
        for keyword in keywords:
            # format for query string
            if " " in keyword:
                keyword = keyword.strip().replace(" ", "+")

            query_string = query_string_creation(parameters)
            start_urls.append("http://{0}.craigslist.org/search/sss?query={1}{2}".format(city, keyword, query_string))
    return start_urls

def generate_individual_list_urls(start_urls):
    """Generate individual list URLs"""
    il_urls = []
    for start_url in start_urls:
        time.sleep(1.23)
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
    list_price = tree.xpath("//span[@class='price']/text()")
    if list_price is None or list_price == []:
        return None
    list_price = list_price[0][1:]

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

    # naive, but just take location from URL
    start_index = url.find("//")
    end_index = url.find(".craigs")
    location = url[start_index + 2:end_index]

    # print (condition, cylinders, drive, fuel, list_price, location, make,
    #        odometer, paint_color, size, title_status, transmission, url, vin)

    return Listing(condition, cylinders, drive, fuel, list_price, location, make, odometer,
                   paint_color, size, title_status, transmission, url, vin)

def run():
    """main"""
    listings = []

    cities = [# "atlanta",
              # "austin",
              # "boston",
              # "chicago",
              "dallas",
              "denver",
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

    keywords = ["mercedes benz sprinter",
                # "minibus",
                # "dodge promaster",
                # "ford transit",
                # "nissan nv",
                # "minibus",
    ]

    parameters = "new,white,sedan,rwd,gas,clean,automatic"

    # json from django
    json_response = json.dumps(
        {"cities":cities,
         "keywords":keywords,
         "parameters":"new"}
    )
    decoded_json = json.loads(json_response)
    cities = decoded_json["cities"]
    keywords = decoded_json["keywords"]
    parameters = decoded_json["parameters"]

    start_urls = generate_start_urls(cities, keywords, parameters)

    for start_url in start_urls:
        print "\n", start_url
    il_urls = generate_individual_list_urls(start_urls)

    for il_url in il_urls:
        # let's not get blacklisted
        time.sleep(1.23)
        listing = parse_page(il_url)
        if listing is not None:
            listings.append(listing)

    for listing in listings:
        print listing.condition, listing.cylinders, listing.drive, listing.fuel, listing.list_price, listing.location, listing.make, listing.odometer, listing.paint_color, listing.size, listing.title_status, listing.transmission, listing.url, listing.vin

if __name__ == "__main__":
    run()
