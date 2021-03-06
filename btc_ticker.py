#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import base64
import cv2
import random
from datetime import datetime
from time import sleep
import requests
import random
from bs4 import BeautifulSoup as bs

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # get the HTTP response and construct soup object
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies

def get_session(proxies):
    # construct an HTTP session
    session = requests.Session()
    # choose one random proxy
    proxy = random.choice(proxies)
    session.proxies = {"http": proxy, "https": proxy}
    return session

url = "http://192.168.100.218:80/post"




# Create background image
fnt1 = ImageFont.truetype("./fonts/Kenney Blocks.ttf",16)
img = Image.new("RGB", (64,64), color=(0,0,0))
d = ImageDraw.Draw(img)
offset=0
fill_btc = (255,255,255)
d.text((16,0+offset),"BTC",font=fnt1, fill=fill_btc)

# send background image to Divoom
img.save("btc_ticker.png")
img = cv2.imread("btc_ticker.png")
# convert image to RGB bit array and encode to base64
img_bytes = img.tobytes()
img_bytes = base64.b64encode(img_bytes)
# payload for Divoom
params = {
    "Command":"Draw/SendHttpGif",
    "PicNum":1,
    "PicWidth":64,
    "PicOffset":0,
    "PicID":1,
    "PicSpeed":0,
    "PicData":img_bytes.decode("iso-8859-1")
}
# send post request to Divoom
#res = requests.post(url, json=params)

while True:
    try:
        res = requests.post(url, json=params)
        api = "https://production.api.coindesk.com/v2/tb/price/ticker?assets=all"
        news = "https://cryptopanic.com/api/v1/posts/?auth_token=2dd0d59a99511263960349afcbe67a4212b66975&kind=news"

        news_data = requests.get(news).json()
        news = news_data['results']
        titles = []

        for n in news:
            info = n['title']
            titles.append(info)

        data  = requests.get(api).json()
        data = data['data']
        chg = round(data["BTC"]['change']['percent'],2)
        price = round(data["BTC"]['ohlc']['c'],0)

        if chg <0 :
            fill= "#ff0000"
        else:
            fill="#00ff00"


        params_price = {"Command":"Draw/SendHttpText",
                        "TextId":1,
                        "x":4,
                        "y":22,
                        "dir":-1,
                        "font":1,
                        "TextWidth":64,
                        "speed":1.0,
                        "TextString":f"${str(price)}",
                        "color":fill
                        }
        params_change = {"Command":"Draw/SendHttpText",
                    "TextId":2,
                    "x":6,
                    "y":36,
                    "dir":-1,
                    "font":1,
                    "TextWidth":64,
                    "speed":1.0,
                    "TextString":f"{str(chg)}%",
                    "color":fill
                    }
        req = requests.post(url, json=params_price)
        req = requests.post(url, json=params_change)
        params_scrolling = {"Command":"Draw/SendHttpText",
                    "TextId":3,
                    "x":0,
                    "y":50,
                    "dir":-1,
                    "font":1,
                    "TextWidth":64,
                    "speed":1.0,
                    "TextString":random.choice(titles),
                    "color":"#ffffff"
                    }
        req = requests.post(url, json=params_scrolling)
        print(f"Last updated on {datetime.now()}, BTC price {price} USD")

        sleep(60*1)
    except:
        print("Could not connect to API")








