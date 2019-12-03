const ajaxLogin = {
	"home": function(){
		$.ajax({
			url : '/',
			type : 'get',
			dataType : 'html',
			success : function(html){
				ajaxLogin.logindiv();
				ajaxLogin.loginnav();
				$("#card_title").html("홈");
				$("#content_page").html("<h2>환영합니다.</h2>");
			},
			error : function() {
			}
		});
	},
	"sign" : function(){
		$.ajax({
			url : '/sign',
			type : 'get',
			dataType : 'html',
			success : function(html){	
				$("#card_title").html("회원가입");
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"signOk" : function(mail, passwd, name, phone, addr){
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
				$("#card_title").html("홈");
				$("#content_page").html("<h2>회원 가입을 성공했습니다.</h2>");
			},
			error : function() {
			}
		});
	},
	"login" : function(){
		$.ajax({
			url : '/login',
			type : 'get',
			dataType : 'html',
			success : function(html){	
				$("#card_title").html("로그인");
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"loginnav" : function(){
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
	"logindiv" : function(){
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
	"loginOk" : function(mail, passwd){
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
				if(json['login_chk'] == 'True'){
					if(json['authority']){
						ajaxLogin.loginnav();
					}
					ajaxLogin.logindiv();
					$("#card_title").html("홈");
					$("#content_page").html("<h2>로그인을 성공했습니다.</h2>");
				}else if(json['login_chk'] == 'False'){
					$("#card_title").html("홈");
					$("#content_page").html("<h2>로그인을 실패했습니다.</h2>");
				}
				
			},
			error : function() {
			}
		});
	},
	"logout" : function(){
		$.ajax({
			url : '/logout',
			type : 'get',
			dataType : 'html',
			success : function(html){
				ajaxLogin.logindiv();
				ajaxLogin.loginnav();
				$("#card_title").html("홈");
				$("#content_page").html("<h2>로그아웃 되었습니다.</h2>");
			},
			error : function() {
			}
		});
	},
};

const ajaxGuset = {
	"sangpum_list" : function(select, page){
		$.ajax({
			url : url_sangpum_list,
			type : 'get',
			data : {
				'msg' : select,
				'page' : page
				},
			dataType : 'html',
			success : function(html){	
				$("#card_title").html("상품 목록");
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"sangpum_detail" : function(num){
		$.ajax({
			url : url_sangpum_detail ,
			type : 'get',
			data : {'msg' : num},
			dataType : 'html',
			success : function(html){	
				$("#card_title").html("");
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"sangpum_order_page" : function(num){
		$.ajax({
			headers: { "X-CSRFToken": token },
			url : sangpum_order_page,
			type : 'post',
			data : {'msg' : num},
			dataType : 'html',
			success : function(html){	
				$("#card_title").html("");
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	}
};
const ajaxJs = {
	"ajax_order_list" : function(select, page){
		$.ajax({
			url : url_order_list,
			type : 'get',
			data : {
				'msg' : select,
				'page' : page
				},
			dataType : 'html',
			success : function(html){	
				$("#card_title").html("주문 목록");
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"ajax_order_detail" : function(num) {
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
	"ajax_stock_list" : function(page) {
		$.ajax({
			url : url_stock_list ,
			type : 'get',
			data : {'page' : page},
			dataTpye : 'html',
			success : function(html){
				$("#card_title").html("재고 목록");
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"ajax_stock_detail" : function(num) {
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
	"ajax_stock_modify" : function(num) {
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
	"ajax_stock_modifyOk" : function(id, name, quantity, price) {
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
				ajaxJs.ajax_stock_list(url_stock_list, $("#now_page").val());
				ajaxJs.ajax_stock_detail(id, url_stock_detail);
			},
			error : function() {
			}
		});
	},
	"ajax_stock_insert_page" : function(){
		$.ajax({
			url : url_stock_insert_page ,
			type : 'get',
			dataTpye : 'html',
			success : function(html){
				$("#card_title").html("재고 추가");
				$("#content_page").html(html);
			},
			error : function() {
			}
		});
	},
	"ajax_stock_insertOk" : function(name, quantity, price) {
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