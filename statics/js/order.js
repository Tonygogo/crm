function formatState(val, row){
    if(val == 1) {
        return "已回款";
    } else {
        return "未回款";
    }
}

function formatAction(val, row) {
    return "<a href='javascript:openOrderDetailsDialog(" + row.id + ")'>查看订单明细</a>"
}

// 打开详情窗体
function openOrderDetailsDialog(orderId) {
	// 加载详细数据
    $.post("../../"+ orderId +"/find/", {},function(result) {
        $("#fm").form('load', result);
        if(result.state == 0 ) {
            $("#state").val("未回款");
        } else if(result.state == 1) {
            $("#state").val("已回款");
        }
    });
 
    // 加载详细列表数据
    $("#dg2").datagrid({
        'url': "../../"+ orderId +"/order_detail/"
    });
    
    // 打开窗体
    $("#dlg").dialog("open").dialog("setTitle","订单明细");
}

function closeOrderDetailsDialog(){
    $("#dlg").dialog("close");
}