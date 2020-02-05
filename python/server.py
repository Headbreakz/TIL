from flask import Flask,request,jsonify
import requests
import json
import urllib
import urllib.parse
from bs4 import BeautifulSoup



def getWeather(city):
    url="https://search.naver.com/search.naver?query="
    url=url+urllib.parse.quote_plus(city + "날씨")
    print(url)
    bs=BeautifulSoup(urllib.request.urlopen(url).read(),"html.parser")
    temp=bs.select('span.todaytemp')
    desc=bs.select('p.cast_txt')
    
    return {"temp":temp[0].text ,"desc":desc[0].text}

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def home():
    res={'fulfillmentText':'hello'}
    return jsonify(res)
#     name = request.args.get("name")
#     return "hello, its me.." 

@app.route('/abc')
def abc():
    return "abc=lotte"

@app.route('/weather')
def weather():
    city=request.args.get("city")
    info=getWeather(city)
    
    return jsonify(info)

@app.route('/dialogflow')
def dialogflow():
    res={'fulfillmentText':'hello'}
    return jsonify(res)



if __name__ == '__main__':
    app.run(host='0.0.0.0' , port = 3000, debug=True)
          