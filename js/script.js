// スクロール時に特定の要素が表示されたときにアニメーションを開始する
$('.effect').on('inview', function() {
    var $item = $(this); // 現在の要素を取得
    $item.addClass('start'); // アニメーションを開始するためのクラスを追加
});

// ヘッダー要素を選択
var $header = $('header');

// ウィンドウの高さを取得
var w_h = $(window).height();
// トップに戻るボタンを選択
var topBtn = $('.to_top');

// モバイルデバイスかどうかをユーザーエージェントで判断
if ((navigator.userAgent.indexOf('iPhone') > 0 && navigator.userAgent.indexOf('iPad') == -1) || navigator.userAgent.indexOf('iPod') > 0 || navigator.userAgent.indexOf('Android') > 0) {
   // モバイル向けのスライドショー設定
   $.sublime_slideshow({
           src:[
           {url:"img/slide/main_img_01_sp.jpg"},
           {url:"img/slide/main_img_02_sp.jpg"},
           {url:"img/slide/main_img_03_sp.jpg"}
           ],
           duration:   5,
           fade:       1,
           scaling:    false,
           rotating:   false,
           // overlay: "img/slide/pattern.png" // この行はコメントアウトされています
       });

   // スクロール時の動作を設定
   $(window).scroll(function () {
       // スクロールが一定量を超えたらトップに戻るボタンを表示
       if ($(this).scrollTop() > 100 && menuOpen == false) {
           topBtn.fadeIn();
       } else {
           topBtn.fadeOut();
       }
   });
} else {
   // PC向けのスライドショー設定
   $.sublime_slideshow({
           src:[
           {url:"img/slide/main_img_01.jpg"},
           {url:"img/slide/main_img_02.jpg"},
           {url:"img/slide/main_img_03.jpg"}
           ],
           duration:   5,
           fade:       1,
           scaling:    1.07,
           rotating:   false,
           // overlay: "img/slide/pattern.png" // この行はコメントアウトされています
       });

   // スクロール時の動作を設定
   $(window).scroll(function () {
       var w_h = $(window).height();
       var s_top = $(this).scrollTop(); // スクロール位置を取得
       var l_top = w_h / 2;
       var ml_top = l_top + s_top / 2;

       // スクロールが一定量を超えたらトップに戻るボタンを表示
       if ($(this).scrollTop() > 100 && menuOpen == false) {
           topBtn.fadeIn();
       } else {
           topBtn.fadeOut();
       }
        // スクロールが更に進んだらヘッダーを固定表示
        if ($(window).scrollTop() > 300) {
               $header.addClass('fixed');
           } else {
               $header.removeClass('fixed');
           }
   });
}

// ページロード時に実行される関数
$(function(){
   // トップに戻るボタンを初期状態で非表示に設定
   topBtn.hide();

   // アンカーリンクがクリックされた時のスムーススクロール設定
   $('a[href^=#]').click(function(){
       var speed = 500;
       var href= $(this).attr("href");
       var target = $(href == "#" || href == "" ? 'html' : href);
       var position = target.offset().top;
       $("html, body").animate({scrollTop:position}, speed, "swing");
       return false;
   });
});

// スクロール時にトップに戻るボタンの位置を調整
$(function(){
   $(window).bind("scroll", function() {
       var scrollHeight = $(document).height();
       var scrollPosition = $(window).height() + $(window).scrollTop();
       var footHeight = $("footer").height(); // フッターの高さ

       // スクロール位置がフッターに到達したらボタンの位置を調整
       if (scrollHeight - scrollPosition <= footHeight) {
           $(".to_top").css({"position":"fixed","bottom": footHeight});
       } else {
           $(".to_top").css({"position":"fixed","bottom": "10px"});
       }
   });
});

// スマホメニューの開閉制御
var bnrBtn = $('#g_navi');
var bnrBtn2 = $('#h_box_sp');
var menuOpen = false; // メニューが開いているかのフラグ
var scrollpos;

$('.bg_bl').hide(); // メニュー背景の初期状態を非表示に設定

var ttt = false; // メニュー開閉の状態を管理する変数

$(function(){
   // メニューボタンがクリックされた時の動作
   $(".menu_btn").on("click", function() {
       if(ttt == false) { // メニューが閉じている状態
           bnrBtn.stop().animate({'left' : '20%'}, 300);
           bnrBtn2.stop().animate({'left' : '0%'}, 300);
           menuOpen = true;
           $('.om').hide();
           $('.to_top').hide();
           $('.bg_bl').fadeIn();
           scrollpos = $(window).scrollTop();
           $('body').addClass('fixed').css({'top': -scrollpos});
           $(".menu_btn").addClass('opened');
           ttt = true;
       } else { // メニューが開いている状態
           bnrBtn.stop().animate({'left' : '100%'}, 300);
           bnrBtn2.stop().animate({'left' : '100%'}, 300);
           menuOpen = false;
           $('.om').show();
           $('.bg_bl').fadeOut();
           $('body').removeClass('fixed').css({'top': 0});
           $(".menu_btn").removeClass('opened');
           window.scrollTo( 0 , scrollpos );
           ttt = false;
       }
   });
});

// メニュー内のリンクがクリックされた時にメニューを閉じる
$('#g_navi a[href]').on('click', function(event) {
   if(ttt == true) {
       $('.menu_btn').trigger('click');
   }
});

// ウィンドウサイズが変更された時のメニュー開閉状態の調整
$(window).resize(function(){
   var w = $(window).width();
   var x = 960;
   if (w >= x) {
       bnrBtn.stop().animate({'left' : '100%'}, 300);
       bnrBtn2.stop().animate({'left' : '100%'}, 300);
       menuOpen = false;
       $('.bg_bl').hide();
       ttt = false;
       $(".menu_btn").removeClass('opened');
   }
});

// アコーディオンメニューの動作
$(function(){
   $(".ac_menu").on("click", function() {
       $(this).next().slideToggle(); // 隣接する要素の表示/非表示を切り替え
       $(this).toggleClass("active"); // アクティブ状態のトグル
   });
});

// サイトアクセス時にボディをフェードイン
$(function(){
   $('body').hide();
   $('body').fadeIn(300);
});

// スクロール時に特定のエフェクトを発生させる（プラグインが必要）
$(window).fadeThis();
