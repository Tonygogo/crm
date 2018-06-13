// 点击搜索
function searchCustomerService() {
    var startCreateDate = $("#s_createDatefrom").datebox("getValue");
    if (startCreateDate != null && startCreateDate.trim().length > 0){
        startCreateDate += ' 00:00:00'
    }
    var endCreateDate = $("#s_createDateto").datebox("getValue");
    if (endCreateDate != null && endCreateDate.trim().length > 0){
        endCreateDate += ' 23:59:59'
    }
    $("#dg").datagrid('load', {
        'customer': $("#s_customer").val(),
        'overview': $("#s_overview").val(),
        'serveType': $("#s_serveType").combobox('getValue'),
        'startCreateDate': startCreateDate,
        'endCreateDate': endCreateDate
    })
}


function openCustomerServiceFileDialog() {
    var selectedRows = $("#dg").datagrid("getSelections");
    if(selectedRows.length != 1) {
        $.messager.alert("系统提示","请选择一条要分配的客户服务数据！");
        return;
    }
    var row = selectedRows[0];
    $("#dlg").dialog("open").dialog("setTitle", "查看服务");
    $("#fm").form("load", row);
}

function closeCustomerFileDialog() {
   $("#dlg").dialog("close");
}