$(document).ready(function(){
	// 주문 리스트에서 select에 대한 이벤트
	$(document).on("change","select[id='ord_state']",function(){
		var select = this.value;
		
		ajaxJs.ajax_order_list(select, '1'); // select되면 페이지는 1로
	});
	// 주문 리스트(검색)에서 select에 대한 이벤트
	$(document).on("change","select[id='os_state']",function(){
		var select = this.value;
		var type = $("#os_type").val()
		var value = $("#os_value").val()
		ajaxJs.ajax_order_list_search(select, '1', type, value);
	});
	// 회원가입하기 버튼 이벤트
	$(document).on("click","button[id='btn_sign_ok']",function(){
		mail = $("#cmail").val();
		passwd= $("#cpasswd").val();
		passwdchk= $("#cpasswdchk").val();
		name = $("#cname").val();
		phone = $("#cphone").val();
		addr = $("#caddr").val();
		ajaxLogin.signOk(mail, passwd, name, phone, addr);
	});
	// 로그인버튼 이벤트
	$(document).on("click","button[id='btn_login_ok']",function(){
		mail = $("#cmail").val();
		passwd= $("#cpasswd").val();

		ajaxLogin.loginOk(mail, passwd);
	});
	// 주문 관리 목록 클릭시 상세보기를 위한 이벤트
	$(document).on("click","tr[name='orders']",function(){
		var num = $(this).attr("id").replace("order_","")
		if($("#pre_order_detail").val() != num){
			ajaxJs.ajax_order_detail(num);
			
			if($("#pre_order_detail").val() != ""){
				$("#order_detail_page_"+$("#pre_order_detail").val()).empty();
				$("#pre_order_detail").val('')
			}
		}else{ // 같은 목록 선택시 상세보기 사라지게하기
			$("#order_detail_page_"+$("#pre_order_detail").val()).empty();
			$("#pre_order_detail").val('')
		}
	});
	// 재고 관리 목록 클릭시 상세보기를 위한 이벤트
	$(document).on("click","tr[name='stocks']",function(){
		var num = $(this).attr("id").replace("stock_","")
		if($("#pre_stock_detail").val() != num){
			ajaxJs.ajax_stock_detail(num);
			if($("#pre_stock_detail").val() != ""){
				$("#stock_detail_page_"+$("#pre_stock_detail").val()).empty();
				$("#pre_stock_detail").val('')
			}	
		}else{
			$("#stock_detail_page_"+$("#pre_stock_detail").val()).empty();
			$("#pre_stock_detail").val('')
		}
	});
	// 상품 상세보기 페이지
	$(document).on("click","tr[name='sangpums']",function(){
		var num = $(this).attr("id").replace("sangpum_","");
		ajaxGuset.sangpum_detail(num);
	});
	// 수정하기 페이지가는 이벤트
	$(document).on("click","button[name='btn_st_modify']",function(){
		var num = $(this).attr("id").replace("stock_","");
		ajaxJs.ajax_stock_modify(num);
	});
	// 수정하기에서 취소 버튼 이벤트
	$(document).on("click","button[name='btn_st_modify_ca']",function(){
		var num = $("form[name=st_modify_frm] input[name=id]").val();
		ajaxJs.ajax_stock_detail(num);
	});
	// 수정하기에서 수정하기 버튼 이벤트
	$(document).on("click","button[name='btn_st_modify_ok']",function(){
		var id = $("form[name=st_modify_frm] input[name=id]").val();
		var name = $("form[name=st_modify_frm] input[name=st_name]").val();
		var quantity = $("form[name=st_modify_frm] input[name=st_quantity]").val();
		var price = $("form[name=st_modify_frm] input[name=st_price]").val();
		ajaxJs.ajax_stock_modifyOk(id, name, quantity, price);
	});
	// 재고 추가하기
	$(document).on("click","button[name='btn_st_insert_ok']",function(){
		var name = $("form[name=st_insert_frm] input[name=st_name]").val();
		var quantity = $("form[name=st_insert_frm] input[name=st_quantity]").val();
		var price = $("form[name=st_insert_frm] input[name=st_price]").val();
		if(name == "" || quantity == "" || price == ""){
			alert('빈칸이 있습니다.')
			return;
		}
		ajaxJs.ajax_stock_insertOk(name, quantity, price);
	});
	// 기본주소지, 최근 주소지
	$(document).on("change","input[name='op_ship']",function(){
		var radio = this.value;
		ajaxGuset.order_cus_addr(radio);
	});
	// 수량 입력(change)
	$(document).on("change ","input[id='sd_quantity']",function(e){
		var quantity = $("#sd_quantity").val();
		if (quantity < 0){ // 0 이하로 입력했을 때 0으로 변경
			quantity = 0;
		}
		
		var price = quantity * $("#sd_price").val(); // 총가격 계산
		price = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		quantity = quantity.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); // 10000 => 10,000
		$("#sd_total").html("총 상품금액(수량) : " + price +"원(" + quantity +"개)");
		$("#sd_submit").prop('href', "javascript:ajaxGuset.sangpum_order_page('" + $("#sd_id").val() +"', '" + $("#sd_quantity").val() + "')")
	});
	// 수량 입력 엔터 비활성화
	$(document).on("keydown ","input[id='sd_quantity']",function(e){
		if (e.keyCode === 13) {
			e.preventDefault();
		}
	});
	// 상품 주문하기 버튼 이벤트
	$(document).on("click","input[id='sop_submit']",function(){
		var name = $("#ord_cname").val();
		var phone = $("#ord_phone").val();
		var addr = $("#ord_addr").val();
		var q = $("#sop_quantity").val();
		var pid = $("#sop_pid").val();
		ajaxGuset.sangpum_orderOk(name, phone, addr, q, pid);
	});
	// 주문 관리에서 주문 상태 변경 이벤트
	$(document).on("click","button[id='od_btn_mod']",function(){
		var name = $(this).attr("name");
		
		if(name == 'n'){ // 수정하기 보여주기
			var str = "<select class='custom-select custom-select-sm mb-4' name='od_state' id='od_state'>";
			str += "<option value='0'>주문</option>";
			str += "<option value='1'>배송</option>";
			str += "<option value='2'>완료</option>";
			str += "</select>";
			$(this).attr("name", "y");
			$("#od_state").html(str);
			$("#od_btn_mod").html("완료");
			$("#od_state option[value=" + $("#od_state_txt").val() +"]").attr("selected", "ture");
		}else if(name == 'y'){ // 수정 완료
			$.ajax({
				headers: { "X-CSRFToken": token },
				url : url_order_change,
				type : 'post',
				data : {
					'state' : $("#od_state option:selected").val(),
					'id' : $("#od_id_txt").val(),
				},
				dataTpye : 'text',
				success : function(text){
					$(this).attr("name", "n");
					s_type = $("#os_type").val();
					s_value = $("#os_value").val();
					if(s_type){					
						ajaxJs.ajax_order_list_search($("#os_state option:selected").val(), $("#now_page").val(), s_type, s_value);
					}
					else{
						ajaxJs.ajax_order_list($("#ord_state option:selected").val(), $("#now_page").val());
					}
				},
				error : function() {
				}
			});
		}
	});
	// 주문 관리 리스트 검색 버튼
	$(document).on("click","input[id='order_search']",function(){
		s_type = $("#s_type option:selected").val();
		s_value = $("#s_value").val();
		ajaxJs.ajax_order_list_search('all', '1', s_type, s_value)
	});
});