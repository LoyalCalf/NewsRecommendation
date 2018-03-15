

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
    function setDiv(item){
    var div = '<li style="padding-top: 0"><div class="item-inner-one item-inner-same g-c"><div><div class="item-inner-img sc-tr">'
        + '<a href=' + item.news_link + '>' + item.title + '</a>'
        + '</div></div></div></li>';
    return div
}

       $.ajax({
           type:'GET',
           dataType:"json",
           url:"api/news_hot/?format=json",
           success :function (data) {
                var listUl=$("#news_id");
                for(var i=1;i<=data.length;i++){
                    var div = setDiv(data[i-1]);
                    // var a=$("<a>"+data.results[i-1].title+"</a>>");
                    // a.attr("href","api/news/"+data.results[i-1].news_id);
                    listUl.append(div);

                }
           },
           error:function (e) {
               alert("失败")
           }
       })

  });

