from tkinter import W
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import requests
import base64
from io import BytesIO
import cv2
import random

from time import sleep
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
res = requests.post(url, json=params)

while True:
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
    req = requests.post(url, json=params_price)
    req = requests.post(url, json=params_change)
    req = requests.post(url, json=params_scrolling)
    sleep(60*1)







print(params)
#print(res.text)

