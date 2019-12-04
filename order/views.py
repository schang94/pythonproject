from django.shortcuts import render
from order.models import Order, Stock, Customer, CusAddr
from django.http.response import HttpResponse, HttpResponseRedirect
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls.base import reverse
from datetime import datetime

# Create your views here.
def MainFunc(request):
    return render(request, 'main.html')

def LoadNav(request):
    return render(request, 'login_nav.html')

def LoadDiv(request):
    return render(request, 'login_div.html')

def SignFunc(request):
    return render(request, 'sign.html')

def SignOkFunc(request):
    Customer(
        cus_mail = request.POST['mail'],
        cus_passwd = request.POST['passwd'],
        cus_name = request.POST['name'],
        cus_phone = request.POST['phone'],
        cus_addr = request.POST['addr'],
        cus_authority = 0
        ).save()
    
    return HttpResponseRedirect('/')

def LoginFunc(request):
    return render(request, 'login.html')

def LoginOkFunc(request):
    mail = request.POST['mail'],
    passwd = request.POST['passwd'],
    print(mail[0], passwd[0])

    try:
        data = Customer.objects.get(cus_mail = mail[0], cus_passwd = passwd[0])
        request.session['name'] = data.cus_mail
        request.session['authority'] = data.cus_authority
        data = {
            "login_chk" : 'True',
            "authority" : data.cus_authority
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    except:
        data = {
            "login_chk" : 'False',
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

def LogoutFunc(request):
    del request.session['name']
    del request.session['authority']
    
    return render(request, 'main.html')

def SangpumFunc(request):
    state = request.GET['msg']
    
    if state == 'all':
        sdatas = Stock.objects.all().order_by('id')
    else:
        sdatas = Stock.objects.filter(state = state).order_by('id')
    
    total_len = len(sdatas) # 전체 목록 갯수
    paginator = Paginator(sdatas, 5)
    
    try:
        page = request.GET.get('page')
    except:
        page = 1
    
    try:
        data = paginator.page(page)
    except PageNotAnInteger:        # 페이지가 정수가 아닌 경우
        data = paginator.page(1)
    except EmptyPage:               # 페이지가 받아지지 않을 경우
        data = paginator.page(paginator.num_pages())

    index = data.number - 1
    max_index = len(paginator.page_range)

    start_index = index - 2 if index >= 2 else 0
    
    if index < 2:
        end_index = 5 - start_index
    else:
        end_index = index + 3 if index <= max_index - 3 else max_index
    
    page_range = list(paginator.page_range[start_index:end_index])
    
    state = {0:'주문', 1:'배송', 2:'완료'}
    return render(request, 'sangpum_list.html', {'sangpum_data' : data, 'ostate' : state, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index})

def SangpumDetail(request):
    num = request.GET['msg']
    
    sdata = Stock.objects.get(id = num)
    return render(request, 'sangpum_detail.html', {"sangpum_data" : sdata})

def SangpumOrder(request):
    num = request.POST['num']
    id = request.POST['id']
    
    try:
        request.session['name']
        sdata = Stock.objects.get(id = id)
        cdata = Customer.objects.get(cus_mail = request.session['name'])
        return render(request, 'sangpum_order_page.html', {"sangpum_data" : sdata, "cus_data": cdata,"quantity":num})
    except:
        return render(request, 'login.html')
        
def CusAddrFunc(request):
    radio = request.POST['radio']
    
    try:
        if radio == 'basic':
            addr = Customer.objects.get(cus_mail = request.session['name'])
            data = {
                "ord_cname" : addr.cus_name,
                "ord_addr" : addr.cus_addr,
                "ord_phone" : addr.cus_phone,
            }
        elif radio == 'recent':
            addr = CusAddr.objects.filter(ca_mail = request.session['name']).order_by('-id')[0]
            data = {
                "ord_cname" : addr.ca_name,
                "ord_addr" : addr.ca_addr,
                "ord_phone" : addr.ca_phone,
            }
    except:
        data = {
            "ord_cname" : "",
            "ord_addr" : "",
            "ord_phone" : "",
        }
    
    return HttpResponse(json.dumps(data), content_type="application/json")

def SangpumOrderOkFunc(request):
    Order(
        ord_cname = request.POST['name'],
        ord_addr = request.POST['addr'],
        ord_phone = request.POST['phone'],
        ord_quantity = request.POST['q'],
        state = 0,
        ord_date = datetime.now(),
        ord_cid = Customer.objects.get(cus_mail = request.session['name']),
        ord_pid = Stock.objects.get(id = request.POST['pid'])
        ).save()
        
    CusAddr(
        ca_name = request.POST['name'],
        ca_addr = request.POST['addr'],
        ca_phone =request.POST['phone'],
        ca_mail = Customer.objects.get(cus_mail = request.session['name'])
        ).save()
    
    sdata = Stock.objects.get(id = request.POST['pid'])
    sdata.st_quantity -= int(request.POST['q'])
    sdata.save()
    data = {"ok":True}
    return HttpResponse(json.dumps(data), content_type="application/json")
    
def OrderList(request):
    state = request.GET['msg']
    
    if state == 'all':
        odatas = Order.objects.all().order_by('-id')
    else:
        odatas = Order.objects.select_related('ord_cid', 'ord_pid').filter(state = state).order_by('-id')
    
    total_len = len(odatas) # 전체 목록 갯수
    paginator = Paginator(odatas, 5)
    
    try:
        page = request.GET.get('page')
    except:
        page = 1
    
    try:
        data = paginator.page(page)
    except PageNotAnInteger:        # 페이지가 정수가 아닌 경우
        data = paginator.page(1)
    except EmptyPage:               # 페이지가 받아지지 않을 경우
        data = paginator.page(paginator.num_pages())

    index = data.number - 1
    max_index = len(paginator.page_range)

    start_index = index - 2 if index >= 2 else 0
    
    if index < 2:
        end_index = 5 - start_index
    else:
        end_index = index + 3 if index <= max_index - 3 else max_index
    
    page_range = list(paginator.page_range[start_index:end_index])
    
    state = {0:'주문', 1:'배송', 2:'완료'}
    return render(request, 'order_list.html', {'order_data' : data, 'ostate' : state, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index})

def OrderDetail(request):
    num = request.GET['msg']

    odata = Order.objects.get(id = num)
    
    state = {0:'주문', 1:'배송', 2:'완료'}
    return render(request, 'order_detail.html', {'order_data' : odata, 'ostate' : state})

def StockList(request):
    
    sdatas = Stock.objects.all().order_by('-id')
    
    total_len = len(sdatas)
    paginator = Paginator(sdatas, 5)
    
    try:
        page = request.GET.get('page')
    except:
        page = 1
    
    try:
        data = paginator.page(page)
    except PageNotAnInteger:        # 페이지가 정수가 아닌 경우
        data = paginator.page(1)
    except EmptyPage:               # 페이지가 받아지지 않을 경우
        data = paginator.page(paginator.num_pages())

    index = data.number - 1
    max_index = len(paginator.page_range)

    start_index = index - 2 if index >= 2 else 0
    
    if index < 2:
        end_index = 5 - start_index
    else:
        end_index = index + 3 if index <= max_index - 3 else max_index
    
    page_range = list(paginator.page_range[start_index:end_index])
    
    return render(request, 'stock_list.html', {'stock_data' : data, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index})

def StockDetail(request):
    num = request.GET['msg']

    sdata = Stock.objects.get(id = num)
    
    return render(request, 'stock_detail.html', {'stock_data' : sdata})

def StockModify(request):
    num = request.GET['msg']

    sdata = Stock.objects.get(id = num)

    return render(request, 'stock_modify.html', {'stock_data' : sdata})

def StockModifyOk(request):
    id = request.POST['id']
    name = request.POST['name']
    quantity = request.POST['quantity']
    price = request.POST['price']
    
    sdata = Stock.objects.get(id = id)
    sdata.st_name = name
    sdata.st_quantity = quantity
    sdata.st_price = price
    sdata.save()

    return HttpResponse('True')

def StockInsert(request):
    return render(request, 'stock_insert.html')

def StockInsertOk(request):
    Stock(
        st_name = request.GET['name'],
        st_quantity = request.GET['quantity'],
        st_price = request.GET['price']
        ).save()
        
    
    return HttpResponse(reverse('stock_list'))