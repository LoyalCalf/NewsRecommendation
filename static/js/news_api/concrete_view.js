$(document).ready(function () {
    var num = obtainNum();

     function setTemplate(item){
        var template ='<div class="panel panel-danger">'+
                '<div class="panel-heading">'+
                  '<h3 class="panel-title">'+item.title+'</h3>'+
                '</div>'+
                '<div class="panel-body">'+item.html_content+
                  '</div>'+
               '</div>';
        return template
}

     function obtainNum() {
         var src=window.location.href;
         var url=src.split("/");
         return url[url.length-2]
     }


       $.ajax({
           type:'GET',
           dataType:"json",
           url:"http://127.0.0.1:8000/api/news/"+ num,
           success :function (data) {
               var listUl=$("#news-content");
               var  item=setTemplate(data);
               listUl.append(item);
           },
           error:function (e) {
               alert("失败")
           }
       })

  });