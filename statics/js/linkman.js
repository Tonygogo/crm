$(function() {
    $("#dg").edatagrid({
        url:'../linkman_select/',
        saveUrl:'../linkman_add/',
        updateUrl:'../linkman_update/',
        destroyUrl:'../linkman_delete/',
        onBeforeSave:function () {
            // 执行前。。。
        }
    });
});

// 添加行
function add() {
    $("#dg").edatagrid('addRow');
}
// 删除行
function deleteLinkman() {
    $("#dg").edatagrid('destroyRow');
}
// 取消航
function cancelRow() {
    $("#dg").edatagrid('cancelRow');
}

// 提交保存数据
function save() {
    $("#dg").edatagrid('saveRow');
    setTimeout(function(){
        $('#dg').datagrid('acceptChanges');
        $('#dg').edatagrid('reload');
    },1000)

}