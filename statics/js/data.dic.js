function searchDataDic() {
    $("#dg").datagrid('load', {
        'dataDicName': $("#s_dataDicName").combobox('getValue'),
        'dataDicValue': $("#s_dataDicValue").val()
    })
}

function openAddDialog() {
    $("#dlg").dialog('setTitle', '添加数据字典').dialog('open')
}

function openModifyDialog() {
    // 获取选中行
    var rows = $("#dg").datagrid('getSelections');
    if (rows.length != 1) {
        $.messager.alert('提示', '请选择一行进行修改！')
        return
    }
    // 给表单赋值
    $("#fm").form('load', rows[0]);
    $("#dlg").dialog('setTitle', '修改数据字典').dialog('open')
}

function deleteDataDic() {
     // 获取选中行
    var rows = $("#dg").datagrid('getSelections');
    if (rows.length == 0) {
        $.messager.alert('提示', '请选择一行进行删除！')
        return
    }
    var ids = [];
    for (var i =0; i <rows.length; i++){
        ids.push(rows[i].id)
    }
    $.messager.confirm('确认框', '确定要删除这[<font color="red">'+ ids.length +'</font>]数据吗？', function(r){
        if (r){
            $.post('../delete_datadic/', {'ids': ids.join(',')}, function(resp){
                $.messager.alert('提示', resp.message);
                if (resp.code == 1){
                    $("#dg").datagrid('reload') // 重新加载
                }
            })
        }
    });


}

function saveDataDic() {
    if (!$("#fm").form('validate')) {
        return;
    }
    var dataDicName = $("#dataDicName").combobox('getValue');
    var dataDicValue = $("#dataDicValue").val();
    var id = $("#id").val();
    var url = '../add_datadic/';
    var data = {'dataDicName': dataDicName, 'dataDicValue': dataDicValue};
    if (id != null ){
        url =  '../update_datadic/';
        data.id = id
    }
    $.post(url, data, function(resp){
        $.messager.alert('提示', resp.message);
        if (resp.code == 1){
            closeDataDic(); // 关闭窗体
            $("#dg").datagrid('reload') // 重新加载
        }
    })
}

function closeDataDic() {
    $("#fm").form('clear')
   $("#dlg").dialog('close')
}