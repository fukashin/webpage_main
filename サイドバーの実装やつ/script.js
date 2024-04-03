// DOMが読み込まれたら実行される関数
document.addEventListener('DOMContentLoaded', () => {
    fetchMainContent();
});

// メインコンテンツを非同期で読み込む関数
function fetchMainContent() {
    fetch('main_content.html') // メイン記事のHTMLファイル
        .then(response => response.text())
        .then(html => {
            document.getElementById('main-content').innerHTML = html;
        })
        .catch(error => {
            console.error('Error fetching main content:', error);
        });
}
