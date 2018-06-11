function searchCustomer(){
    $("#dg").datagrid('load', {
        customerName: $("#s_customerName").val(),
        customerNo: $("#s_customerNo").val()
    })
}

// 打开添加窗体
function openAddDialog() {
    $("#dlg").dialog('open').dialog('setTitle', '添加客户信息');
}

// 打开修改窗体
function  openModifyDialog() {

    // 获取选中的修改的记录信息
    var rows = $("#dg").datagrid('getSelections');
    if (rows.length != 1) {
        $.messager.alert('提示', '请选择一条记录进行修改！')
        return
    }
    var row = rows[0];
    // 给表单赋值
    $("#fm").form('load', row);

    $("#dlg").dialog('open').dialog('setTitle', '修改客户信息');
}

// 关闭窗体
function closeCustomerDialog(){
    // 清除表单数据
    $("#fm").form('clear');
    $("#dlg").dialog('close');
}

// 保存
function saveCustomer() {
    var id = $("#id").val()
    var url = '../add/';
    if (id != null && !isNaN(parseInt(id))) {
        url = '../update/';
    }
    $("#fm").form('submit', {
        url: url,
        onSubmit: function(){
            // do some check表单数据
            return $(this).form('validate');
        },
        success:function(data){
            console.log(typeof data);
            data = JSON.parse(data);// 把json字符串转化成json对象
            $.messager.alert('提示', data.message);
             if (data.code == 1) {
                 $("#dg").datagrid('reload');
                 closeCustomerDialog();
             }
        }
    });
}

// 删除
function deleteCustomer() {
    // 先获取要删除的记录
    var rows = $("#dg").datagrid('getSelections')

    // 判断是否有选中
    if (rows.length == 0) {
        $.messager.alert('提示', '请至少选择一条记录进行删除！')
        return;
    }
    // 获取删除的记录主键
    var ids = []
    for (var i=0; i < rows.length; i++) {
        ids.push(rows[i].id);
    }

    // 弹出确认框后删除
    $.messager.confirm('确认提示', '确认要删除这<font color="red">['+ ids.length +']</font>条记录吗？',
        function(r){
            if (r){
                $.post('../delete/', {ids:ids.join(',')}, function(resp){
                    $.messager.alert('提示', resp.message);
                    if (resp.code == 1) {
                        $("#dg").datagrid('reload')
                    }
                })
            }
    })
}

// 联系人管理
function openCustomerLinkMan() {
    var rows = $("#dg").datagrid('getSelections');
    if (rows.length != 1) {
        $.messager.alert('提示', '请选择一条记录进行查询！')
        return
    }
    row = rows[0];
    var customerId = row.id
    window.parent.openTab('客户联系人管理', '/customer/'+ customerId +'/linkman_index/', 'icon-lxr')
}

function openCustomerContact() {
var rows = $("#dg").datagrid('getSelections');
    if (rows.length != 1) {
        $.messager.alert('提示', '请选择一条记录进行查询！')
        return
    }
    row = rows[0];
    var customerId = row.id
    window.parent.openTab('客户交往记录管理', '/customer/'+ customerId +'/contact_index/', 'icon-jwjl')
}

function openCustomerOrder() {

}