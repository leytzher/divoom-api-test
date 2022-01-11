from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import base64
import cv2
import random
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
#d.text((16,0+offset),"BTC",font=fnt1, fill=fill_btc)

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

    #news_data = requests.get(news).json()
    try:
        # get proxies
        proxies = get_free_proxies()
        s = get_session(proxies)
        print("Trying with proxy")
        news_data = s.get(news, timeout=1.5).json()
        print(news_data)
    except:
        print("Proxy error on news")
        news_data = requests.get(news).json()
    news = news_data['results']
    titles = []
    for n in news:
        info = n['title']
        titles.append(info)

    try:
        # get proxies
        proxies = get_free_proxies()
        s = get_session(proxies)
        data = s.get(api, timeout=1.5).json()
    except:
        print("Proxy error on price")
        data  = requests.get(api).json()
    data = data['data']
    chg = round(data["BTC"]['change']['percent'],2)
    price = round(data["BTC"]['ohlc']['c'],0)

    otherCoins = ""
    for coin in ["ETH","ADA","XRP","SOL"]:
        txt = f"- {coin}:{round(data[coin]['ohlc']['c'],1)}$ {round(data[coin]['change']['percent'],2)}%)"
        otherCoins+=txt


    if chg <0 :
        fill= "#ff0000"
    else:
        fill="#00ff00"


    params_price = {"Command":"Draw/SendHttpText",
                        "TextId":1,
                        "x":4,
                        "y":26,
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
                    "y":38,
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

    params_scrolling2 = {"Command":"Draw/SendHttpText",
                    "TextId":4,
                    "x":0,
                    "y":0,
                    "dir":-1,
                    "font":1,
                    "TextWidth":64,
                    "speed":1.0,
                    "TextString":random.choice(titles),
                    "color":"#ffffff"
                    }
    params_scrolling3 = {"Command":"Draw/SendHttpText",
                    "TextId":5,
                    "x":0,
                    "y":14,
                    "dir":0,
                    "font":1,
                    "TextWidth":64,
                    "speed":1.0,
                    "TextString":otherCoins,
                    "color":"#ff00ff"
                    }
    req = requests.post(url, json=params_scrolling)
    req = requests.post(url, json=params_scrolling2)
    req = requests.post(url, json=params_scrolling3)
    sleep(60*1)








