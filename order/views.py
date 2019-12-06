from django.shortcuts import render
from order.models import Order, Stock, Customer, CusAddr
from django.http.response import HttpResponse, HttpResponseRedirect
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls.base import reverse
from datetime import datetime

# Create your views here.
def MainFunc(request): # 메인 페이지로 이동
    return render(request, 'main.html')

def LoadNav(request): # 이것저것 목록
    return render(request, 'login_nav.html')

def LoadDiv(request): # 로그인 목록
    return render(request, 'login_div.html')

def SignFunc(request): # 회원가입 페이지로 이동
    return render(request, 'sign.html')

def SignOkFunc(request): # 회원가입 실행
    Customer(
        cus_mail = request.POST['mail'],
        cus_passwd = request.POST['passwd'],
        cus_name = request.POST['name'],
        cus_phone = request.POST['phone'],
        cus_addr = request.POST['addr'],
        cus_authority = 0
        ).save()
    
    return HttpResponseRedirect('/')

def LoginFunc(request): # 로그인 페이지 이동
    return render(request, 'login.html')

def LoginOkFunc(request): #로그인
    mail = request.POST['mail'],
    passwd = request.POST['passwd'],

    try:
        # 정보 확인
        data = Customer.objects.get(cus_mail = mail[0], cus_passwd = passwd[0])
        # 성공시 세션 생성
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

def LogoutFunc(request): # 로그아웃(세션 삭제)
    del request.session['name']
    del request.session['authority']
    
    return render(request, 'main.html')

def SangpumFunc(request): # 상품 리스트
    sdatas = Stock.objects.all().order_by('id')
    
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
    max_index = len(paginator.page_range) # 최대 페이지

    start_index = index - 2 if index >= 2 else 0 # 페이징에서 첫번째로 보여질 페이지
    
    # 페이징에서 마지막에 보여질 페이지
    if index < 2:
        end_index = 5 - start_index
    else:
        end_index = index + 3 if index <= max_index - 3 else max_index
    
    # 보여지는 페이지
    page_range = list(paginator.page_range[start_index:end_index])
    
    state = {0:'주문', 1:'배송', 2:'완료'}
    return render(request, 'sangpum_list.html', {'sangpum_data' : data, 'ostate' : state, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index})

def SangpumDetail(request): # 상품 상세보기
    num = request.GET['msg']
    
    sdata = Stock.objects.get(id = num)
    return render(request, 'sangpum_detail.html', {"sangpum_data" : sdata})

def SangpumOrder(request): # 상품 주문 페이지 이동
    num = request.POST['num']
    id = request.POST['id']
    
    # 로그인 상태 확인하고 안되어 있으면 로그인 페이지로 이동
    try:
        request.session['name']
        sdata = Stock.objects.get(id = id)
        cdata = Customer.objects.get(cus_mail = request.session['name'])
        return render(request, 'sangpum_order_page.html', {"sangpum_data" : sdata, "cus_data": cdata,"quantity":num})
    except:
        return render(request, 'login.html')
        
def CusAddrFunc(request): # 주문하기에서 radio버튼에 대한 view
    radio = request.POST['radio']
    
    try:
        if radio == 'basic': # 기본 주소지
            addr = Customer.objects.get(cus_mail = request.session['name'])
            data = {
                "ord_cname" : addr.cus_name,
                "ord_addr" : addr.cus_addr,
                "ord_phone" : addr.cus_phone,
            }
        elif radio == 'recent': # 최근 주문한 주소지
            addr = CusAddr.objects.filter(ca_mail = request.session['name']).order_by('-id')[0]
            data = {
                "ord_cname" : addr.ca_name,
                "ord_addr" : addr.ca_addr,
                "ord_phone" : addr.ca_phone,
            }
    except: # 등록된 주소지가 없으면 공백으로 출력
        data = {
            "ord_cname" : "",
            "ord_addr" : "",
            "ord_phone" : "",
        }
    
    return HttpResponse(json.dumps(data), content_type="application/json")

def SangpumOrderOkFunc(request): # 주문하기
    # 주문 테이블에 저장
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
    
    # 최근 주소지 저장
    CusAddr(
        ca_name = request.POST['name'],
        ca_addr = request.POST['addr'],
        ca_phone =request.POST['phone'],
        ca_mail = Customer.objects.get(cus_mail = request.session['name'])
        ).save()
    
    # 재고량 변화
    sdata = Stock.objects.get(id = request.POST['pid'])
    sdata.st_quantity -= int(request.POST['q'])
    sdata.save()
    
    return HttpResponseRedirect("/")
    
def OrderList(request): # 주문 관리 페이지 리스트
    st = request.GET['msg']
    
    if st == 'all': # 전체 목록으로 선택했을 떄
        odatas = Order.objects.all().order_by('-id')
    else: # 배송, 주문, 완료 목록으로 선택했을 때
        odatas = Order.objects.filter(state = st).order_by('-id')
    
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
    return render(request, 'order_list.html', {'order_data' : data, 'ostate' : state, 'st' : st, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index})

def OrderDetail(request): # 주문 내용 상세보기
    num = request.GET['msg']

    odata = Order.objects.get(id = num)
    
    state = {0:'주문', 1:'배송', 2:'완료'}
    return render(request, 'order_detail.html', {'order_data' : odata, 'ostate' : state})

def OrderListSearch(request): # 주문 목록 검색
    st = request.GET['msg']
    s_type = request.GET['type']
    s_value = request.GET['value']
    print(st, s_type, s_value)
    try:
        if st == 'all': # 전체 목록으로 선택했을 때
            if s_type == 'cname': # 구매자로 검색 했을 떄
                odatas = Order.objects.filter(ord_cid__cus_mail__contains = s_value).order_by('-id')
            elif s_type == 'pname': # 상품명으로 검색했을 떄
                odatas = Order.objects.filter(ord_pid_id__st_name__contains = s_value).order_by('-id')
        else: # 배송, 주문, 완료 목록으로 선택했을 때
            if s_type == 'cname': # 구매자로 검색 했을 떄
                odatas = Order.objects.filter(ord_cid__cus_mail__contains = s_value, state = st).order_by('-id')
            elif s_type == 'pname': # 상품명으로 검색했을 떄
                odatas = Order.objects.filter(ord_pid_id__st_name__contains = s_value, state = st).order_by('-id')
    except:
        odatas = ""
    
    
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
    search = {'st':st, 'type':s_type, 'value':s_value}
    return render(request, 'order_search_list.html', {'order_data' : data, 'ostate' : state, 'st' : search, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index})

def OrderChage(request): # 주문 상태 변경
    state = request.POST['state']
    id = request.POST['id']
    
    odata = Order.objects.get(id = id)
    odata.state = state
    odata.save()
    
    st = {'0':'주문', '1':'배송', '2':'완료'}
    return HttpResponse(st[state])

def StockList(request): # 재고 목록
    
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

def StockDetail(request): # 재고 상세 보기
    num = request.GET['msg']

    sdata = Stock.objects.get(id = num)
    
    return render(request, 'stock_detail.html', {'stock_data' : sdata})

def StockModify(request): # 재고 수정 페이지
    num = request.GET['msg']

    sdata = Stock.objects.get(id = num)

    return render(request, 'stock_modify.html', {'stock_data' : sdata})

def StockModifyOk(request): # 재고 수정하기
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

def StockInsert(request): # 재고 추가하기 페이지
    return render(request, 'stock_insert.html')

def StockInsertOk(request): # 재고 추가하기
    Stock(
        st_name = request.GET['name'],
        st_quantity = request.GET['quantity'],
        st_price = request.GET['price']
        ).save()
        
    
    return HttpResponse(reverse('stock_list'))