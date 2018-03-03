$(document).ready(function () {

       //  var  information ={
       //     new_id:$("#news_id").val(information.new_id),
       //     new_link:$("#news_link").val(information.new_link),
       //     source:$("#source").val(information.source),
       //     title:$("#item-inner-title").val(information.title),
       //     abstract:$("#abstract").val(information.abstract),
       //     tag:$("#tag").val(information.tag),
       //     classification:$("#classification").val(information.classification)
       // };
        alert("执行ajax函数之前");
       $.ajax({
           type:'GET',
           dataType:"json",
           url:"api/news/?format=json",
           success :function (data) {
                var listUl=$("#news_id");
                for(var i=1;i<=data.results.length;i++){
                    var a=$("<a>"+data.results[i-1].title+"</a>>");
                    a.attr("href","api/news/"+data.results[i-1].news_id);
                    listUl.append(a);
                }
           },
           error:function (e) {
               alert("失败")
           }
       })

  });