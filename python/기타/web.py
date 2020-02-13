from flask import Flask,request,jsonify

app = Flask(__name__)
cnt=0



@app.route('/',methods=['POST','GET'])
def home():
    
    html = """
    <iframe
    allow="microphone;"
    width="350"
    height="430"
    src="https://console.dialogflow.com/api-client/demo/embedded/headbreakz">
    </iframe>
    """  
    
    return html + "<img src=/static/hi.gif />"



@app.route('/counter')
def counter():
    global cnt
    cnt += 1
    return f"{cnt}명이 방문했습니다."


@app.route('/counter1')
def counter1():
      
    global cnt
    cnt +=1
    
    """
    html=""
    for i in str(cnt):
    html +=f"<img src=/static/noname{i}.gif width=32>"
    html += "얏호"
    """
    
    html = "".join([f"<img src=/static/noname{i}.gif width=500>" for i in str(cnt) ])
    html += "얏호"
    
    return html

@app.route('/weather',methods=["POST","GET"])
def weather():
    if request.method =="GET":
        req=request.args
    else :
        req=request.form
        
    city = req.get("city")
#     city = request.args.get("city")
#     city=request.form.get("city")
    return f"{city} 날씨 좋앙"
    
    
           
          


if __name__ == '__main__':
    app.run(host='0.0.0.0' , port = 3000, debug=True)