function resetValue(){
    $("#serveType").combobox("setValue","");
    $("#customer").val("");
    $("#overview").val("");
    $("#serviceRequest").val("");
}

function saveCustomerService(){
    var url = "../../add/";
    $("#fm").form("submit",{
        url : url,
        onSubmit: function(){
            return $(this).form("validate");
        },
        success:function(result) {
            var result = JSON.parse(result);
            $.messager.alert("系统提示", result.message);
            if(result.code == 1) {
                resetValue();
            }
        }
    });
}
