function searchProduct(){
    $("#dg").datagrid('load', {
        'productName': $("#s_productName").val()
    })
}

// 添加按钮
function openAddDialog() {
    $("#dlg").dialog('setTitle', '添加产品信息').dialog('open')
}

// 修改按钮
function openModifyDialog() {
    // 1、获取选中的一行
    // 2、给form表单赋值
    // 3、弹出
}

// 删除按钮
function deleteProduct() {
    // 1、获取选中的行
    // 2、遍历得到主键集合
    // 3、请求后台进行删除，回调函数进行刷新
}

// 保存按钮
function saveProduct() {
    // 要根据id的值判断是新增还是修改，如果新增就是新增的url，如果是修改就是修改的url
    // 提交表单到各自的url中请求数据，在回调后刷新数据列表
}

// 关闭窗体
function closeProductDialog() {
    // 1、要清空表单
    // 2、关闭弹出框
}