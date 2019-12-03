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
});