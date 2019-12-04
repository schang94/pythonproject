$(document).ready(function(){
	$(document).on("change","select[id='ord_state']",function(){
		var select = this.value;
		
		ajaxJs.ajax_order_list(select, '1');
	});
	$(document).on("click","button[id='btn_sign_ok']",function(){
		mail = $("#cmail").val();
		passwd= $("#cpasswd").val();
		passwdchk= $("#cpasswdchk").val();
		name = $("#cname").val();
		phone = $("#cphone").val();
		addr = $("#caddr").val();
		ajaxLogin.signOk(mail, passwd, name, phone, addr);
	});
	$(document).on("click","button[id='btn_login_ok']",function(){
		mail = $("#cmail").val();
		passwd= $("#cpasswd").val();

		ajaxLogin.loginOk(mail, passwd);
	});
	$(document).on("click","tr[name='orders']",function(){
		var num = $(this).attr("id").replace("order_","")
		if($("#pre_order_detail").val() != num){
			ajaxJs.ajax_order_detail(num);
			
			if($("#pre_order_detail").val() != ""){
				$("#order_detail_page_"+$("#pre_order_detail").val()).empty();
				$("#pre_order_detail").val('')
			}
		}else{
			$("#order_detail_page_"+$("#pre_order_detail").val()).empty();
			$("#pre_order_detail").val('')
		}
	});
	
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
	
	$(document).on("click","tr[name='sangpums']",function(){
		var num = $(this).attr("id").replace("sangpum_","");
		ajaxGuset.sangpum_detail(num);
	});
	
	$(document).on("click","button[name='btn_st_modify']",function(){
		var num = $(this).attr("id").replace("stock_","");
		ajaxJs.ajax_stock_modify(num);
	});
	
	$(document).on("click","button[name='btn_st_modify_ca']",function(){
		var num = $("form[name=st_modify_frm] input[name=id]").val();
		ajaxJs.ajax_stock_detail(num);
	});
	
	$(document).on("click","button[name='btn_st_modify_ok']",function(){
		var id = $("form[name=st_modify_frm] input[name=id]").val();
		var name = $("form[name=st_modify_frm] input[name=st_name]").val();
		var quantity = $("form[name=st_modify_frm] input[name=st_quantity]").val();
		var price = $("form[name=st_modify_frm] input[name=st_price]").val();
		ajaxJs.ajax_stock_modifyOk(id, name, quantity, price);
	});
	$(document).on("click","button[name='btn_st_insert_ok']",function(){
		var name = $("form[name=st_insert_frm] input[name=st_name]").val();
		var quantity = $("form[name=st_insert_frm] input[name=st_quantity]").val();
		var price = $("form[name=st_insert_frm] input[name=st_price]").val();
		ajaxJs.ajax_stock_insertOk(name, quantity, price);
	});
	
	$(document).on("change","input[name='op_ship']",function(){
		var radio = this.value;
		ajaxGuset.order_cus_addr(radio);
	});
	$(document).on("change","input[id='sd_quantity']",function(){
		var price = $("#sd_quantity").val() * $("#sd_price").val();
		price = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		$("#sd_total").html("총 상품금액(수량) : " + price +"원(" + $("#sd_quantity").val() +"개)");
		$("#sd_submit").prop('href', "javascript:ajaxGuset.sangpum_order_page('" + $("#sd_id").val() +"', '" + $("#sd_quantity").val() + "')")
	});
	
	$(document).on("click","input[id='sop_submit']",function(){
		var name = $("#ord_cname").val();
		var phone = $("#ord_phone").val();
		var addr = $("#ord_addr").val();
		var q = $("#sop_quantity").val();
		var pid = $("#sop_pid").val();
		ajaxGuset.sangpum_orderOk(name, phone, addr, q, pid);
	});
});