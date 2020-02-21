from django.conf import settings
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import connection

from . import forms
from . import models
from . import apps


def page(request):
    datas = [{"id":1,"name":"길동맨1"},
             {"id":2,"name":"길동맨2"},
             {"id":3,"name":"길동맨3"},
             {"id":4, "name":"길동맨4"},
             {"id":5, "name":"길동맨5"},
             {"id":6, "name":"길동맨6"},
             ]

    page = request.GET.get("page",1)
    p = Paginator(datas,3)
    subs=p.page(1)

    return render(request, "myboard/page.html", {"datas":datas})

class LoginView(View):
    def get(self, request):
        return render(request, apps.APP+"/login.html")

    def post(self, request):
        #Loging 처리
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user == None :
            return redirect('login_board')    #urls.py에서 지정한 name. NOT 경로명.

        #로그인 성공한 경우
        request.session['username'] = username
        return redirect(apps.APP+'all/0/list')

class BoardView(View):
    def get(self, request, category, pk, mode):
        if mode == 'add':
            form = forms.BoardForm()
        elif mode == 'list':
            username = request.session["username"]
            user = User.objects.get(username=username)
            data = models.Board.objects.all().filter(category=category)

            context = {"data": data, "username": username, "category": category}
            return render(request, apps.APP + "/list.html", context)
        elif mode == "detail":
            p = get_object_or_404(models.Board, pk=pk)
            p.cnt += 1
            p.save()
            return render(request, apps.APP + "/detail.html", {"d": p, "category": category})
        elif mode == "edit":
            post = get_object_or_404(models.Board, pk=pk)
            form = forms.BoardForm(instance=post)
        else:
            return HttpResponse("error page")

        return render(request, apps.APP + "/edit.html", {"form": form})

    def post(self, request, category, pk, mode):

        username = request.session["username"]
        user = User.objects.get(username=username)

        if pk == 0:
            form = forms.BoardForm(request.POST)
        else:
            post = get_object_or_404(models.Board, pk=pk)
            form = forms.BoardForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            if pk == 0:
                post.author = user
            post.category = category
            post.save()
            return redirect("myboard", category, 0, 'list')
        return render(request, apps.APP + "/edit.html", {"form": form})

def ajaxdel(request):

    pk=request.GET.get("pk")

    board=models.Board.objects.get(pk=pk)
    board.delete()
    return JsonResponse({'error':'0'})

def ajaxget(request):
    page = request.GET.get("page",1)

    datas=models.Board.objects.all().filter(category='common')
    # p=Paginator(datas,3)
    page=int(page)
    subs=datas[(page-1)*3:(page)*3]

    datas = {"datas":[{'pk': sub.pk,'title':sub.title,'cnt':sub.cnt} for sub in subs]}
    return JsonResponse(datas)


def dictfetchall(cursor):
    desc=cursor.description
    return[
        dict(zip([col[0] for col in desc],row))
        for row in cursor.fetchall()
    ]

def listsql(request,category,page):

    username = request.session["username"]
    cursor = connection.cursor()
    cursor.execute(f"""select title, cnt, username,category 
                   from myboard_board b , auth_user u 
                   where b.author_id = u.id and username='{username}' and category='{category}'
                   """
                   )
    sub_find=dictfetchall(cursor)

    subs= sub_find[(page - 1)*3:(page)*3]

    context = {"datas": [{'title': sub['title'], 'cnt': sub['cnt'], 'username': sub['username']} for sub in subs]}

    return render(request,'myboard/list3.html',context)

def photo(request):

    username = request.session["username"]
    sql = f"""
        select filename
        from myboard_image 
        where author_id=(select id from auth_user where username='{username}')
        """

    cursor = connection.cursor()
    cursor.execute(sql)

    data = dictfetchall(cursor)
    context = {"data": data, "username": username}

    return render(request, 'myboard/photo.html', context)



def uploadimage(request):
    file = request.FILES['filename']
    username = request.POST["username"]
    filename = file.name
    fp = open(settings.BASE_DIR + '/static/faces/'+username +"/"+ filename, 'wb')
    for chunk in file.chunks():
        fp.write(chunk)
    fp.close()

    sql = f"""
    INSERT INTO myboard_image
    ("author_id", "filename")
    VALUES((select id from auth_user where username='{username}'),'{filename}');
    """

    cursor = connection.cursor()
    cursor.execute(sql)


    return redirect('/myboard/photo')
