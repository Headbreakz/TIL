from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.paginator import Paginator

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
