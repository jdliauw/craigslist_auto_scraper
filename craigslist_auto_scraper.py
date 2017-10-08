import requests
from lxml import html
from bs4 import BeautifulSoup

class Listing:
    condition = None
    cylinders = None
    drive = None
    fuel = None
    location = None
    odometer = None
    paint_color = None
    size = None
    title_status = None
    transmission = None
    url = None
    vin = None

    def __init__(condition, cylinders, drive, fuel, location, odometer, paint_color, size, title_status, transmission, url, vin):
        self.condition = condition
        self.cylinders
        self.drive
        self.fuel
        self.location
        self.odometer
        self.paint_color
        self.size
        self.title_status
        self.transmission
        self.url
        self.vin

urls = []

cities = [
        # "atlanta",
        # "austin",
        # "boston",
        # "chicago",
        # "dallas",
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
        # "sfbay"
    ]

keywords = [
    "mercedes benz sprinter",
    # "dodge promaster",
    "ford transit",
    # "nissan nv",
    # "minibus"
]

def generate_start_urls():
    start_urls = []
    for city in cities:
        for keyword in keywords:
            if " " in keyword:
                kws = keyword.split(" ")
                keyword = ""
                for kw in kws:
                    keyword += kw +  "+"
                keyword = keyword[:-1]
            start_urls.append("http://{0}.craigslist.org/search/sss?query={1}".format(city, keyword))
    return start_urls

def generate_individual_list_urls(start_urls):
    il_urls = []
    for start_url in start_urls:
        page = requests.get(start_url)
        tree = html.fromstring(page.content)
        il_urls += tree.xpath("//a[@class='result-title hdrlnk']/@href")
    return il_urls

def parse_page(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    spans = tree.xpath("//p[@class='attrgroup']/span")
    for span in spans:
        print span.text, span.xpath("b/text()")


if __name__ == "__main__":
    # start_urls = generate_start_urls()
    # il_urls = generate_individual_list_urls(start_urls)
    parse_page("https://portland.craigslist.org/clc/ctd/d/2006-dodge-sprinter-2500/6324920484.html")
