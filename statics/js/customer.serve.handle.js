// 打开处理的对话框
function openCustomerServiceProceDialog(){
    // 获取选中的记录
    var rows = $("#dg").datagrid('getSelections');
    if (rows.length != 1){
        $.messager.alert('提示', '请选择一条记录进行处理！');
        return
    }
    var row = rows[0];
    $("#fm").form('load', row);
    $("#serviceProceTime").val(new Date().format('yyyy-MM-dd hh:mm:ss'));
    $("#serviceProcePeople").val($("#loginUserName").val());
    $("#state").val('已处理');
    // 打开对话框
    $("#dlg").dialog('setTitle', '处理客户服务').dialog('open');

}


// 保存
function saveCustomerServiceProce(){
   $("#fm").form("submit",{
        url: "../../update/",
        onSubmit:function() {
            return $(this).form("validate");
        },
        success:function(result) {
            var result = JSON.parse(result);
            if(result.code == 1) {
                $.messager.alert("系统提示","处理成功！");
                $("#serviceProce").val('')
                $("#dlg").dialog("close");
                $("#dg").datagrid("reload");
            } else {
                $.messager.alert("系统提示","处理失败！");
                return;
            }
        }
    });
}


function closeCustomerProceDialog(){
    $("#serviceProce").val('')
    $("#dlg").dialog('close');
}