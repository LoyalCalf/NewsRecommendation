$(document).ready(function () {
        // alert("执行ajax函数之前");
       $.ajax({
           type:'GET',
           dataType:"json",
           url:"api/news/?format=json&limit=10",
           success :function (data) {
               var listUl=$("#news_id");
               for(var i=0;i<data.results.length;i++){
                   var  item=setDiv(data.results[i])
                   listUl.append(item);
                }
                downRollAction();
                classRecommendation();
           },
           error:function (e) {
               alert("失败")
           }
       });

  });

 function setDiv(item){
        if(item.image)
        {
            var img = item.image.split(",")[0];
        }
        var template ='<ul class="news-list" id='+item.news_id+'><li style="padding-top: 0">'+
                            '<div class="item-inner-one item-inner-same g-c">'+
                                '<div>'+
                                    '<div class="item-inner-img sc-tr">'+
                                        '<a class="news_img" target="_blank" href=' + item.news_link + ' >'+
                                            '<img  src='+img+ '>'+
                                        '</a>'+
                                        '<div class="pictext" style="text-align: left;text-indent: 2em; "></div>'+
                                    '</div>'+
                                    '<div class="item-inner-title">'+
                                        '<span class="item-inner-center">'+
                                            '<p>' +
                                                // '<a class="it-news-tl" href="http://www.chinanews.com/" id="title" >'+item.source+'</a>'+
                                                '<a class="it-news-tl" href=/news/'+item.news_id+'>' + item.title + '' +'</p>'+
                                            '<p class="it-news-footer">'+
                                                '<a class="item-news-type item-news-same" id="classification" href="#">'+item.classification+'</a>'+
                                                '<a class="item-news-icon item-news-same" href="#"></a>'+
                                                '<a href="http://www.chinanews.com/" class="item-news-same item-news-name">'+item.source+'</a>'+
                                            '</p>'+
                                        '</span>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'+
                        '</li>'+
                    '</ul>';

        return template
}

//给页面绑定滚动轴事件，当页面下拉到最下层时进行动态请求更新页面
function downRollAction(){
    $(window).scroll(function () {
        var scrollTop = $(this).scrollTop();
        var scrollHeight = $(document).height();
        var windowHeight = $(this).height();
        if (scrollTop + windowHeight === scrollHeight) {
            //当下拉到页面最下端时
            //暂时不添加任何提示样式，通过ajax 和 alert进行调试
            $.ajax({
                type:'GET',
                dataType:"json",
                url:"api/news/?format=json&limit=10&offset="+$("#news_id").children().length,
                success :function (data) {
                    var listUl=$("#news_id");
                    for(var i=0;i<data.results.length;i++){
                    var  item = setDiv(data.results[i])
                    listUl.append(item);
                }
                },
                error:function (e) {
                    alert("失败")
                }
            });
        }
    });
}

function upRollAction(){
    //给刷新按钮绑定函数
     $("#reflesh").click(function(){
        $.ajax({
            type:'GET',
            dataType:"json",
            url:"api/news_recommendation/?format=json&limit=10&offset="+$("#news_id").children().length,
            success :function (data) {
                var listUl=$("#news_id");
                for(var i=0;i<data.results.length;i++){
                    var  item = setDiv(data.results[i]);
                    listUl.append(item);
                }
            },
            error:function (e) {
            alert("失败")
        }});
     });
}

//根据不同种类的新闻进行不同种类的请求
function classRecommendation(){
    $(".newsClass").click(function(){
        $.ajax({
            type:'GET',
            dataType:"json",
            url:"api/news/?format=json&limit=10&classification="+$(this).attr("id"),
            success :function (data) {
                var listUl=$("#news_id");
                listUl.empty();
                for(var i=0;i<data.results.length;i++){
                    var  item = setDiv(data.results[i]);
                    listUl.append(item);
                }
            },
            error:function (e) {
                alert("失败")
         }});
    });
}