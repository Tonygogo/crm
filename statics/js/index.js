$(document).ready(function(){
    $("#submitBtn").click(function(){
        var username = $("#username").val();
        var password = $("#password").val();
        if (username == null || username.trim().length == 0){
            alert('请输入账号');
            return;
        }
        if (password == null){
            alert('请输入密码');
            return;
        }
        var csrfToken = $("#csrf-token").val();
        var params = {username:username, password: password, 'csrfmiddlewaretoken': csrfToken}
        $.post('/system/login/', params, function(resp){
            console.log(resp)
            if (resp.code == 0) {
                alert(resp.message)
            } else if(resp.code == 1) {
                alert(resp.message)
                window.location.href = '/main/'
            }else {
                alert(resp.message)
                window.location.href = '/main/'
            }

        })

    });
});