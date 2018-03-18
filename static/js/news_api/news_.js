$(document).ready(function () {



     function setDiv(item){

        var template ='<ul class="news-list" id='+item.news_id+'><li style="padding-top: 0">'+
                            '<div class="item-inner-one item-inner-same g-c">'+
                                '<div>'+
                                    '<div class="item-inner-img sc-tr">'+
                                        '<a class="news_img" target="_blank" href=' + item.news_link + ' >'+
                                            '<img  src='+item.image+ '>'+
                                        '</a>'+
                                        '<div class="pictext" style="text-align: left;text-indent: 2em; "></div>'+
                                    '</div>'+
                                    '<div class="item-inner-title">'+
                                        '<span class="item-inner-center">'+
                                            '<p>' +
                                                // '<a class="it-news-tl" href="http://www.chinanews.com/" id="title" >'+item.source+'</a>'+
                                                '<a class="it-news-tl" href=' + item.news_link + '>' + item.title + '</a>' +'</p>'+
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

        // alert("执行ajax函数之前");
       $.ajax({
           type:'GET',
           dataType:"json",
           url:"api/news/?format=json",
           success :function (data) {
               var listUl=$("#news_id");
               for(var i=0;i<=data.results.length;i++){
                   var  item=setDiv(data.results[i])
                   listUl.append(item);
              }
           },
           error:function (e) {
               alert("失败")
           }
       })

  });