$("#dg").edatagrid({
    url: '../select_reprieve/',
    saveUrl: '../add_reprieve/',
    updateUrl: '../update_reprieve/',
    destroyUrl: '../delete_reprieve/'
});

function confirmLoss(){
    $.messager.prompt('提示信息', '请输入流失的原因：', function(r){
        if (r){
            $.post('../confirm_loss/', {'lossReason': r}, function(resp){
                $.messager.alert('提示', resp.message)
            })
        }
    });

}