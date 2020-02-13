from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def index(request):
    return HttpResponse("helllllllllllllllllllllllllllllllllllll")

def test(request):
    data = {"s":{"img":"test.png"},"list":[1,2,3,4,5]}
    return render(request,'template.html',data)


def login(request):
    id=request.GET["id"]
    pwd=request.GET["pwd"]
    if id ==pwd :
        request.session["user"]=id
        return redirect("/service")
    return redirect("/static/login.html")

def logout(request):
    request.session["user"]=""
    request.session.pop("user")
    return redirect("/static/login.html")

def service(request):
    if request.session.get("user","") == "" :        
        return redirect("/static/login.html")
    
    html = "Main Servive<br>" + request.session.get("user") + "떙유맨"
    
    return HttpResponse(html)

import face
@csrf_exempt
def uploadimage(request):   

    file = request.FILES['file1']
    filename = file._name    
    fp = open(settings.BASE_DIR + "/static/" + filename, "wb")
    for chunk in file.chunks() :
        fp.write(chunk)
    fp.close()
    
    result = face.facerecognition(settings.BASE_DIR + "/known.bin", settings.BASE_DIR + "/static/" + filename)
    print(result)
    if result != "" : 
        request.session["user"] = result[0]    
        return redirect("/service")
    return redirect("/static/login.html")