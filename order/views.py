from django.shortcuts import render
from order.models import Order, Stock, Customer
from django.http.response import HttpResponse, HttpResponseRedirect
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls.base import reverse

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
        request.session['name'] = data.cus_name
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
    num = request.POST['msg']
    print("뷰 접근 성공")
    try:
        request.session['name']
        sdata = Stock.objects.get(id = num)
        print('0')
        return render(request, 'sangpum_order_page.html', {"sangpum_data" : sdata, "quantity":num})
    except:
        print('1')
        return render(request, 'login.html')
        

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