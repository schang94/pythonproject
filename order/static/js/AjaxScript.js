const ajaxLogin = {
	"home": function(){ // 홈으로 이동하기
		$.ajax({
			url : '/',
			type : 'get',
			dataType : 'html',
			success : function(html){
				ajaxLogin.logindiv();
				ajaxLogin.loginnav();
				var str = '<div class="card-header bg-dark text-white">';
				str += '<h4 class="my-0 font-weight-normal">홈</h4></div>';
				str += '<div class="card-body" >';
				str += '<h2>환영합니다.</h2></div>';
				
				$("#content_page").html(str);
			},
			error : function() {
			}
		});
	},
	"sign" : function(){ // 회원가입 페이지
		$.ajax({
			url : '/sign',
			type : 'get',
			dataType : 'html',
			success : function(html){	
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"signOk" : function(mail, passwd, name, phone, addr){ // 회원가입
		$.ajax({
			headers: { "X-CSRFToken": token },
			url : '/signok',
			type : 'post',
			data : {
				'mail' : mail,
				'passwd' : passwd,
				'name' : name,
				'phone' : phone,
				'addr' : addr
			},
			dataType : 'html',
			success : function(html){
				$("#content_page").html("<h2>회원 가입을 성공했습니다.</h2>");
			},
			error : function() {
			}
		});
	},
	"login" : function(){ // 로그인 페이지
		$.ajax({
			url : '/login',
			type : 'get',
			dataType : 'html',
			success : function(html){	
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"loginnav" : function(){ // 목록(홈, 상품, 주문,재고)
		$.ajax({
			url : '/loadnav',
			type : 'get',
			dataType : 'html',
			success : function(html){
				$("#login_nav").html(html);
			},
			error : function() {
			}
		});
	},
	"logindiv" : function(){ // 목록(로그인,로그아웃,회원가입)
		$.ajax({
			url : '/loaddiv',
			type : 'get',
			dataType : 'html',
			success : function(html){
				$("#login_div").html(html);
			},
			error : function() {
			}
		});
	},
	"loginOk" : function(mail, passwd){ // 로그인
		$.ajax({
			headers: { "X-CSRFToken": token },
			url : '/loginok',
			type : 'post',
			data : {
				'mail' : mail,
				'passwd' : passwd,
			},
			dataType : 'json',
			success : function(json){
				if(json['login_chk'] == 'True'){ // 로그인 성공
					if(json['authority']){ // 관리자 일 떄
						ajaxLogin.loginnav();
					}
					ajaxLogin.logindiv();
					$("#content_page").html("<h2>로그인을 성공했습니다.</h2>");
				}else if(json['login_chk'] == 'False'){ // 로그인 실패
					$("#content_page").html("<h2>로그인을 실패했습니다.</h2>");
				}
				
			},
			error : function() {
			}
		});
	},
	"logout" : function(){ // 로그아웃
		$.ajax({
			url : '/logout',
			type : 'get',
			dataType : 'html',
			success : function(html){
				ajaxLogin.logindiv();
				ajaxLogin.loginnav();
				$("#content_page").html("<h2>로그아웃 되었습니다.</h2>");
			},
			error : function() {
			}
		});
	},
};

const ajaxGuset = {
	"sangpum_list" : function(page){ // 상품리스트
		$.ajax({
			url : url_sangpum_list,
			type : 'get',
			data : {
				'page' : page
				},
			dataType : 'html',
			success : function(html){	
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"sangpum_detail" : function(num){ // 상품 상세보기
		$.ajax({
			url : url_sangpum_detail ,
			type : 'get',
			data : {'msg' : num},
			dataType : 'html',
			success : function(html){	
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"sangpum_order_page" : function(id, num){ // 상품 주문 페이지
		if(num < 1){ // 0이하의 수를 입력했을 때
			alert('구매수량이 올바르지 않습니다.');
			return;
		}
		if($("#sd_quantity_total").val() - num < 0){ // 재고량 보다 많이 주문 했을 때
			alert('재고량이 부족합니다.');
			return;
		}
		
		$.ajax({
			headers: { "X-CSRFToken": token },
			url : url_sangpum_order_page,
			type : 'post',
			data : {
				'id' : id,
				'num' : num},
			dataType : 'html',
			success : function(html){	
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"order_cus_addr" : function(radio){ // 주문 페이지에서 배송 정보 불러오기
		$.ajax({
			headers: { "X-CSRFToken": token },
			url : '/cusaddr',
			type : 'post',
			data : {'radio' : radio},
			dataType : 'json',
			success : function(json){	
				$("#ord_cname").val(json['ord_cname'])
				$("#ord_phone").val(json['ord_phone'])
				$("#ord_addr").val(json['ord_addr'])
			},
			error : function() {
			}
		});
	},
	"sangpum_orderOk" : function(name, phone, addr, q, pid){ // 상품 주문

		$.ajax({
			headers: { "X-CSRFToken": token },
			url : '/orderok',
			type : 'post',
			data : {
				'name' : name,
				'phone' : phone,
				'addr' : addr,
				'q' : q,
				'pid' : pid
			},
			dataType : 'html',
			success : function(html){
				$("#content_page").html("<h2>주문 되었습니다.</h2>");
			},
			error : function() {
			}
		});
	},
};
const ajaxJs = {
	"ajax_order_list" : function(select, page){ // 주문 관리 리스트
		$.ajax({
			url : url_order_list,
			type : 'get',
			data : {
				'msg' : select,
				'page' : page
				},
			dataType : 'html',
			success : function(html){	
				$("#content_page").html(html);
				$("#ord_state option[value=" + select +"]").attr("selected", "ture"); // select의 selected 설정

			},
			error : function() {
			}
		});
	},
	"ajax_order_list_search" : function(select, page, type, value){ // 주문 관리 리스트 검색
		$.ajax({
			url : url_order_list_search,
			type : 'get',
			data : {
				'msg' : select,
				'page' : page,
				'type' : type,
				'value' : value
				},
			dataType : 'html',
			success : function(html){	
				$("#content_page").html(html);
				$("#os_state option[value=" + select +"]").attr("selected", "ture"); // select의 selected 설정
				$("#s_type option[value=" + type +"]").attr("selected", "ture"); // select의 selected 설정
				$("#s_value").val(value);
			},
			error : function() {
			}
		});
	},
	"ajax_order_detail" : function(num) { // 주문 관리 상세보기
		$.ajax({
			url : url_order_detail ,
			type : 'get',
			data : {'msg' : num},
			dataTpye : 'html',
			success : function(html){
				$("#order_detail_page_"+num).html(html);
				$("#pre_order_detail").val(num)
			},
			error : function() {
			}
		});
	},
	"ajax_stock_list" : function(page) { // 재고 관리 리스트
		$.ajax({
			url : url_stock_list ,
			type : 'get',
			data : {'page' : page},
			dataTpye : 'html',
			success : function(html){
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"ajax_stock_detail" : function(num) { // 재고 관리 상세보기
		$.ajax({
			url : url_stock_detail,
			type : 'get',
			data : {'msg' : num},
			dataTpye : 'html',
			success : function(html){
				$("#stock_detail_page_"+num).html(html);
				$("#pre_stock_detail").val(num)
			},
			error : function() {
			}
		});
	},
	"ajax_stock_modify" : function(num) { // 재고 관리 수정 페이지
		$.ajax({
			url : url_stock_modify_page,
			type : 'get',
			data : {'msg' : num},
			dataTpye : 'html',
			success : function(html){
				$("#stock_detail_page_"+num).html(html);
				$("#pre_stock_detail").val(num)
			},
			error : function() {
			}
		});
	},
	"ajax_stock_modifyOk" : function(id, name, quantity, price) { // 재고 관리 수정
		$.ajax({
			headers: { "X-CSRFToken": token },
			url : url_stock_modify_ok ,
			type : 'post',
			data : {
				'id' : id,
				'name' : name,
				'quantity' : quantity,
				'price' : price
			},
			dataTpye : 'text',
			success : function(text){
				ajaxJs.ajax_stock_list($("#now_page").val());
				ajaxJs.ajax_stock_detail(id);
			},
			error : function() {
			}
		});
	},
	"ajax_stock_insert_page" : function(){ // 재고 관리 추가 페이지
		$.ajax({
			url : url_stock_insert_page ,
			type : 'get',
			dataTpye : 'html',
			success : function(html){
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"ajax_stock_insertOk" : function(name, quantity, price) { // 재고 관리 추가
		$.ajax({
			url : url_stock_insert_ok ,
			type : 'get',
			data : {
				'name' : name,
				'quantity' : quantity,
				'price' : price
			},
			dataTpye : 'text',
			success : function(text){
				ajaxJs.ajax_stock_list(text, '1')
			},
			error : function() {
			}
		});
	},
};