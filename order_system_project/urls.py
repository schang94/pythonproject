"""order_system_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from order import views
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainFunc, name='home'),
    path('loadnav', views.LoadNav),
    path('loaddiv', views.LoadDiv),
    path('sign', views.SignFunc),
    path('signok', views.SignOkFunc),
    path('login', views.LoginFunc),
    path('loginok', views.LoginOkFunc),
    path('logout', views.LogoutFunc),
    path('cusaddr', views.CusAddrFunc),
    path('orderok', views.SangpumOrderOkFunc),
    path('sangpum', views.SangpumFunc, name='sanpum_list'),
    path('sangpumdetail', views.SangpumDetail, name='sangpum_detail'),
    path('sangpumorder', views.SangpumOrder, name='sangpum_order_page'),
    path('order/', include('order.urls')),
]
