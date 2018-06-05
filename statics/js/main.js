// 打开dialog对话框
function openPasswordModifyDialog() {
    $("#dlg").dialog('open').dialog('setTitle', '修改密码');
}

// 点击保存
function modifyPassword() {
    // 可以使用form表单校验
    var oldPassword = $("#oldPassword").val();
    if (oldPassword == null || oldPassword == '') {
        alert('请输入原密码');
        return;
    }
    var newPassword = $("#newPassword").val();
    if (newPassword == null || newPassword == '') {
        alert('请输入新密码');
        return;
    }
    var confirmNewPassword = $("#newPassword2").val();
    if (confirmNewPassword == null || confirmNewPassword == '') {
        alert('请输入确认密码');
        return;
    }
    if (newPassword != confirmNewPassword) {
        alert('两次密码输入不相等');
        return;
    }
    var csrfToken = $("#csrf-token").val();
    var params = {
        old_password: oldPassword, new_password: newPassword,
        confirm_new_password: confirmNewPassword, 'csrfmiddlewaretoken': csrfToken
    };
    $.ajax({
        url: '/system/update_password/',
        data: params,
        dataType: 'json',
        type: 'POST',
        success: function (resp) {
            console.log(resp);
            alert(resp.message);
            if (resp.code != 0) {
                window.location.href = '/system/logout/';
            }
        }
    })

}

// 关闭dialog
function closePasswordModifyDialog() {
    $("#oldPassword").val('');
    $("#newPassword").val('');
    $("#newPassword2").val('');
    $("#dlg").dialog('close')
}

// 点击安全退出
function logout() {
    /*
    var r = window.confirm('您确认要退出吗？')
    if (r){
        alert('退出')
    }*/
    $.messager.confirm('确认', '您确认想要退出吗？', function (r) {
        if (r) {
            // $.messager.alert('提示', '退出系统')
            window.location.href = '/system/logout'
        }
    });
}