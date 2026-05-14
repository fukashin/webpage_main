// 作品カードのモーダル表示
(function() {
  document.addEventListener('click', function(e) {
    var card = e.target.closest('.work-card');
    if (card) {
      var modalId = card.getAttribute('data-modal');
      var modal = document.getElementById(modalId);
      if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    }

    // 閉じるボタン or オーバーレイクリックで閉じる
    if (e.target.classList.contains('modal-close') || e.target.classList.contains('modal-overlay')) {
      var overlay = e.target.closest('.modal-overlay') || e.target;
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  });

  // ESCキーで閉じる
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      var active = document.querySelector('.modal-overlay.active');
      if (active) {
        active.classList.remove('active');
        document.body.style.overflow = '';
      }
    }
  });
})();
