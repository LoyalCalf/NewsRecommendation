
(function () {
  var $zhanWei = $('.index-lf-zhanwei');
  var $indexLfHeight = $('.index-lf').outerHeight(true);
  var $indexLfWidth = $('.index-lf').outerWidth(true);
  var $jinCaiPic = $('.jincai-pic');
  var $jinCaiPicHeight = $jinCaiPic.outerHeight(true);
  /*监听页面滚动的函数*/
  function scrollListening(ele,outerHeight) {
    var $ele = $(ele);
    var eleTop = $ele.offset().top;
    if(outerHeight){
      eleTop = eleTop + 50 + $ele.outerHeight(true);
    }
    $(window).scroll(function (e) {
      var scrollTop = $(window).scrollTop();
      if(outerHeight){
        if(scrollTop >= eleTop){
          $('.rg-scroll-one').css({
            'width':340,
            'height':$jinCaiPicHeight,
            'position':'relative',
            'top':0,
            'display':'block',
            'margin-bottom':'16px'
          });
          $jinCaiPic.css({
            'position':'fixed',
            'top':0
          })
        }else{
          $('.rg-scroll-one').css({'display':'none'});
          $jinCaiPic.css('position','relative')
        }
      }else{
        if(scrollTop >= eleTop){
          $ele.css({'top':0, 'position':'fixed'} );
          $zhanWei.css({'display':'block', 'height':$indexLfHeight, 'width':$indexLfWidth})
        }else{
          $ele.css({'top':0, 'position':'relative'});
          $zhanWei.css({'display':'none','height':0, 'width':0})
        }
      }
    });
  }
  
  $(document).ready(function () {
      scrollListening('.index-lf');
      scrollListening('.company',true);
  });
 
  

})();