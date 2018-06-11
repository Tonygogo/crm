$(function() {
	var cusId = $("#cusId").val();
    $("#dg").edatagrid({
        url: '../select_contact/',
        saveUrl: '../add_contact/',
        updateUrl: '../update_contact/',
        destroyUrl: '../delete_contact/',
        pagination: true, // 分页
        pageSize: 10 // 每页条数

    });
});

// 添加一行
function addContact() {
	$('#dg').edatagrid('addRow');
}

// 保存行
function saveContact() {
	$('#dg').edatagrid('saveRow');
	$('#dg').edatagrid('reload');
}

// 删除行
function deleteContact() {
	$('#dg').edatagrid('destroyRow');
}

//撤销行
function cancelRow() {
	$('#dg').edatagrid('cancelRow');
}
