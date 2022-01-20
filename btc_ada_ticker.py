#!/usr/bin/env python
import requests
import base64
import cv2
import random
from datetime import datetime
from time import sleep
import requests
import random
from bs4 import BeautifulSoup as bs


url = "http://192.168.100.218:80/post"

colors = ["#fff7d1","#fffceb","#fff3b7","#ffee9d","#ffea83","#ffe568","#ffe14e","#ffdc34"]

tick = True

while True:
    try:
        if tick == True:
            img = cv2.imread("btc_ticker.png")
        else:
            img = cv2.imread("ada_ticker.png")

        img_bytes = img.tobytes()
        img_bytes = base64.b64encode(img_bytes)

        params = {
            "Command":"Draw/SendHttpGif",
            "PicNum":1,
            "PicWidth":64,
            "PicOffset":0,
            "PicID":1,
            "PicSpeed":0,
            "PicData":img_bytes.decode("iso-8859-1")
        }

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
        if tick:
            coin = "BTC"
            price = round(data[coin]['ohlc']['c'],0)
        else:
            coin = "ADA"
            price = round(data[coin]['ohlc']['c'],3)

        chg = round(data[coin]['change']['percent'],2)

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
                    "color": random.choice(colors)
                    }
        req = requests.post(url, json=params_scrolling)
        print(f"Last updated on {datetime.now()}, BTC price {price} USD")

        tick = not(tick)
        sleep(60*1)
    except:
        print("Could not connect to API")








