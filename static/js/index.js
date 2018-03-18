
(function () {
    var bannerImgArc = ['images/banner_1.jpg','images/banner_2.jpg','images/banner_3.jpg','images/banner_4.jpg','images/banner_5.jpg','images/banner_6.jpg']; //轮播图src
    var bannerTitle = ['要闻','社会','娱乐','体育','军事','名星'];
    var bannerIndex = 0;  //轮播图下标
    var $barCtr= $('.bar-container');  //轮播图容器
    var bannerId;

    function bannerPic() {
        var $imgCta = $('.img-cta');
        var $imgNav = $('.img-nav');

        for(var i = 0; i < bannerImgArc.length; i++){
            $imgCta.append('<img class="bannerImg" src='+ bannerImgArc[i] +'/>');
            $imgNav.append('<div class="nar-title"><a class="bar-nav-item">'+ bannerTitle[i] +'</a></div>');
        }
        var $bannerImg = $('.bannerImg');  //轮播图
        var $narNavItem = $('.bar-nav-item');   //分页器
        $bannerImg.eq(bannerIndex).css({'display':'block'});
        $narNavItem.eq(bannerIndex).addClass('bar-active');

        /**
         * 轮播图的动态切换
         * @param index
         */
        function bannerLoop(index) {
            $bannerImg.eq(index).css({'display':'block'}).fadeIn("500").siblings().css({"display":"none"});
            $narNavItem.removeClass('bar-active').eq(index).addClass('bar-active');
        }

        bannerId = setInterval(function () {
            bannerIndex++;
            if(bannerIndex === bannerImgArc.length){
                bannerIndex = 0;
            }
            bannerLoop(bannerIndex);  //切换
        },3000);

        $barCtr.hover(function (event) {
            clearInterval(bannerId);
        },function (event) {
            // setInterval(bannerId);
            bannerId = setInterval(function () {
                bannerIndex++;
                if(bannerIndex === bannerImgArc.length){
                    bannerIndex = 0;
                }
                bannerLoop(bannerIndex);  //切换
            },3000);
        });

        $narNavItem.on('mouseover',function (e) {
            bannerIndex = $narNavItem.index(this);
            bannerLoop(bannerIndex);
        })
    }
    /*搜索框的焦点的判断*/
    var $sInput = $('.s-search');
    var $lianXiang = $('.s-search-lianxiang');
    var $indexMore = $('.index-lf-more');
    var $indexMoreUl = $('.index-lf-more-ul');
    function inputAddClick() {
        $sInput.focus(function () {
            $lianXiang.css('display','block');
        });
        $sInput.blur(function () {
            $lianXiang.css('display','none');
        });
    }

    /**
     * 封装的hover方法
     * @param ele
     * @param ele1
     */
    function moreHover(ele, ele1) {
        if(ele1){
            ele.hover(function () {
                ele1.css('display','block');
            },function () {
                ele1.css('display','none');
            });
        }else{
            ele.hover(function () {
                ele.css('display','block');
            },function () {
                ele.css('display','none');
            });
        }
    }
    //index-more hover显示
    function indexMoreHover() {
        moreHover($indexMore, $indexMoreUl);
        moreHover($indexMoreUl);
    }

    var $headerMore  = $('.header-more');
    var $showMore = $('.showMore');
    //header-more hover显示
    function hoverHeaderMore() {
        moreHover($headerMore, $showMore);
        moreHover($showMore);
    }

    /*点击刷新*/
    function refresh() {
        $('.back-top>span').on('click',function () {
            location.reload(true);
        })
    }

    function shareMore() {
        var $shareWrap = $('.share-wrap');
        var $snsbox = $('.snsbox');
        moreHover($shareWrap, $snsbox);
    }



   /* 内容*/



    function init() {
        bannerPic();//轮播图
        inputAddClick(); //搜索框的焦点的判断
        indexMoreHover();//index-more hover显示
        hoverHeaderMore();//header-more hover显示
        refresh();//点击刷新
        shareMore();//分享
    }

    init();

})();