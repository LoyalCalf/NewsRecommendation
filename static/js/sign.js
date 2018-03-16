$(document).ready(function(){
    //给登陆按钮绑定事件
    $("#signIn").click(signIn());
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

//定义注册和登陆按钮的触发函数
function signIn(){
    var username = $("#username").val();
    var password = $("#password").val();
    if(username.length !== 0 && password.length !== 0){
        $.ajax({
            url:'/login',
            type:'POST',
            async:true,    //或false,是否异步
            data:{
                username: username,
                password: password
            },
            timeout:5000,    //超时时间
            dataType:'json',    //返回的数据格式：json/xml/html/script/jsonp/text
            success:function(data){
                if(data.code===200){
                    //这里有待进行商榷，可能有头像框，昵称栏等其他信息，且用户登陆之后推荐信息会发生变化，倾向于重新刷新页面
                    //跳转到新闻界面，传递id参数，在新闻界面进行id参数的解析，生成对应的用户信息
                    document.location = "/news?id=" + data.id;
                }
                else{
                    alert("登陆失败，请检查用户名和密码");
                    //失败时清空password的内容
                    $("#password").val("");
                }
            },
            error:function(xhr){
                console.log('错误');
            },
            complete:function(){
                console.log('登陆成功！');
            }
        })
    }
    else{
        alert("用户名和密码不能为空!!!");
    }
}