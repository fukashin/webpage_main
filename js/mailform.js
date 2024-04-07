$(function(){
	// メールフォームのdt要素を選択
	var mailform_dt = $('#mail_form dl dt');
	
	// 必須または任意のマークを付けるためのループ処理
	for(var i=0; i<mailform_dt.length-1; i++){
		// もし隣接するdd要素が'class'属性に'required'を持っていたら
		if( mailform_dt.eq(i).next('dd').attr('class') == 'required' ){
			// 必須マークを追加
			$('<span/>')
				.text('必須')
				.addClass('required')
				.prependTo($(mailform_dt.eq(i)));
			
			// この部分では何も追加していないが、後で拡張可能なスペースを確保
			$('<span/>')
				.appendTo(mailform_dt.eq(i).next('dd'));
		}else{
			// 任意マークを追加
			$('<span/>')
				.text('任意')
				.addClass('optional')
				.prependTo($(mailform_dt.eq(i)));
		}
	}
	
	// Enterキーを押してもフォームが送信されないようにする
	$('input').on('keydown', function(e){
		if( (e.which && e.which === 13) || (e.keyCode && e.keyCode === 13) ){
			return false; // Enterキーのデフォルトの挙動をキャンセル
		}else{
			return true;
		}
	});
	
	// メール送信ボタンクリック時にバリデーションチェックを実行
	$('#mail_submit_button').click(required_check);
	
	// dt要素からフィールド名を抽出する関数
	function slice_method(dt){
		var span_start = dt.html().indexOf('</span>');
		var span_end = dt.html().lastIndexOf('<span');
		var dt_name = dt.html().slice(span_start+7, span_end);
		return dt_name;
	}
	
	// スクロール位置を決定するための比較関数
	function compare_method(s, e){
		if( s>e ){
			return e;
		}else{
			return s;
		}
	}
	
	// 必須チェックの実行関数
	function required_check(){
		var error = 0; // エラー数
		var scroll_point = $('body').height(); // スクロール位置
		
		// 必須項目が存在するかチェック
		if( $('form#mail_form dd.required').length ){
			
			// 各種入力フィールドに対するバリデーションチェック
			// 以下、具体的なチェック処理（省略）
			
		}
		
		// エラーがない場合の送信確認
		if(error == 0){
			if(window.confirm('送信してもよろしいですか？')){
				
				// フォームに追加の隠しフィールドを挿入してJavaScript経由のアクションを示す
				$('<input />')
					.attr({
						type : 'hidden',
						name : 'javascript_action',
						value : true
					})
					.appendTo(mailform_dt.eq(mailform_dt.length-1).next('dd'));
				
				// 現在のURLを隠しフィールドとして挿入
				var now_url = encodeURI(document.URL);
				$('<input />')
					.attr({
						type : 'hidden',
						name : 'now_url',
						value : now_url
					})
					.appendTo(mailform_dt.eq(mailform_dt.length-1).next('dd'));
				
				// 直前のURLを隠しフィールドとして挿入
				var before_url = encodeURI(document.referrer);
				$('<input />')
					.attr({
						type : 'hidden',
						name : 'before_url',
						value : before_url
					})
					.appendTo(mailform_dt.eq(mailform_dt.length-1).next('dd'));
				
				return true; // 送信を許可
			}else{
				return false; // 送信をキャンセル
			}
		}else{
			// エラーがある場合は指定位置までスクロール
			$('html,body').animate({
				scrollTop : scroll_point-50
			}, 500);
			return false; // 送信をキャンセル
		}
	}
});
