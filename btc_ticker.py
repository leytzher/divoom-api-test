from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import requests
import base64
from io import BytesIO

url = "http://192.168.100.218:80/post"
now = datetime.now()

current_time = now.strftime("%H:%M")
current_date = now.strftime("%d %b:%Y")

data_1m = yf.download(tickers="BTC-USD", period="15m", interval="1m")
close_prev  = data_1m['Close'][-2]
close_1m = data_1m['Close'][-1]
delta_1m = ((close_prev - close_1m)/close_prev)*100
delta_1m = round(delta_1m, 3)
print(close_prev, close_1m, delta_1m)
if delta_1m <0 :
    fill=(255,0,0)
else:
    fill=(0,255,0)

img = Image.new("RGB", (64,64), color=(0,0,0))

fnt1 = ImageFont.truetype("./fonts/Kenney Blocks.ttf",16)
fnt2 = ImageFont.truetype("./fonts/Kenney Blocks.ttf",8)
fnt3 = ImageFont.truetype("./fonts/Kenney Mini.ttf",8)

d = ImageDraw.Draw(img)
offset=1
d.text((16,0+offset),"BTC",font=fnt1, fill=fill)

d.text((4,15+offset),str(int(close_1m)),font=fnt1, fill=fill)
d.text((20,33+offset),str(delta_1m)+"%",font=fnt2, fill=fill)

d.text((10,41+offset),current_date,font=fnt3, fill=(255,255,255))
d.text((25,48+offset),current_time,font=fnt3, fill=(255,255,255))

buffered = BytesIO()
img.save(buffered,format="PNG")
img_str = base64.b64encode(buffered.getvalue())

params = {
    "Command":"Draw/SendHttpGif",
    "PicNum":1,
    "PicWidth":64,
    "PicOffset":0,
    "PicID":2,
    "PicSpeed":0,
    "PicData":img_str.decode('utf-8')
}

res = requests.post(url, json=params)
print(params)
print(res.text)
img.save("btc_ticker.gif")
#Debug

