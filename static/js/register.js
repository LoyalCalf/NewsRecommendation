$(document).ready(function(){
    $("#register").click(Register);
});

//csrf token验证，用于django post请求验证，在使用ajax之前对其进行加载
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

function Register(){
    var username = $("#username").val();
    var password = $("#password").val();
    var passwordRe = $("#confirm_password").val();
    var email = $("#email").val();
    if(username.length === 0 || password.length === 0 || email.length === 0){
        alert("用户名，密码和邮箱不能为空!!");
        return "";
    }
    if(password === passwordRe){
        $.ajax({
            url:'/api/register/',
            type:'POST',
            async:true,    //或false,是否异步
            data:{
                username: username,
                password: password,
                email: email
            },
            timeout:5000,    //超时时间
            dataType:'json',    //返回的数据格式：json/xml/html/script/jsonp/text
            success:function(data){
                if(data.code===200){
                    //当注册成功时，应当直接跳回新闻页面，传递用户的信息到主页面
                    document.location="/";
                }
                else{
                    alert(data.msg);
                    //失败时清空password的内容
                    $("#password").val("");
                }
            },
        })
    }
    else{
        //当两次输入的密码不相同时，将其同时设置为空
        $("#password").val("");
        $("#passwordRe").val("");
        alert("两次输入的密码不相同，请重新输入!!!");
        return "";
    }
}