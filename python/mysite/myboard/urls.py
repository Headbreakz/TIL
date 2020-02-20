from django.urls import path
from . import views
from django.shortcuts import redirect


urlpatterns = [
    path('', views.page),
    path('ajaxdel', views.ajaxdel),
    path('ajaxget', views.ajaxget),
    path('<category>/<int:pk>/<mode>/', views.BoardView.as_view(), name="myboard"),
    path('', lambda request: redirect('myboard', 'common', 0, 'list')),
    path('login/', views.LoginView.as_view(), name="login"),
    # path('list/', views.list, name="list"),
    # path('<int:pk>/detail/', views.detail, name='detail'),
    # path('<int:pk>/edit/', views.PostEditView.as_view(), name="edit"),

]