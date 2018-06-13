// 打开处理的对话框
function openCustomerServiceFeedbackDialog(){
    // 获取选中的记录
    var rows = $("#dg").datagrid('getSelections');
    if (rows.length != 1){
        $.messager.alert('提示', '请选择一条记录进行反馈！');
        return
    }
    var row = rows[0];
    $("#fm").form('load', row);
    $("#state").val('已归档');
    // 打开对话框
    $("#dlg").dialog('setTitle', '处理客户反馈').dialog('open');

}


// 保存
function saveCustomerServiceFeedback(){
   $("#fm").form("submit",{
        url: "../../update/",
        onSubmit:function() {
            return $(this).form("validate");
        },
        success:function(result) {
            var result = JSON.parse(result);
            if(result.code == 1) {
                $.messager.alert("系统提示","反馈处理成功！");
                $("#serviceProceResult").val('');
                $("#myd").combobox('setValue', '');
                $("#dlg").dialog("close");
                $("#dg").datagrid("reload");
            } else {
                $.messager.alert("系统提示","反馈处理失败！");
                return;
            }
        }
    });
}


function closeCustomerFeedbackDialog(){
    $("#serviceProceResult").val('');
    $("#myd").combobox('setValue', '');
    $("#dlg").dialog('close');
}