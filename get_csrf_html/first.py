import requests
from html.parser import HTMLParser

session = requests.Session()

url = "http://172.22.104.5:8080/public"

get_page = session.get(url=url)

class GetterCSFRToken(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag=="meta" and attrs[0][1]=="csrf-token":
            global csrftoken
            csrftoken = attrs[1][1]

parser = GetterCSFRToken()

csrftoken = ''

parser.feed(get_page.text)
print(csrftoken)

session.close()