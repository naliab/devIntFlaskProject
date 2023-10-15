const TRANSLATE_BTN = document.getElementById('translate-btn');
const ARTICLE_TXT_ELEM = document.getElementById('article-content');
const ARTICLE_TITLE_ELEM = document.getElementById('article-title');

TRANSLATE_BTN.addEventListener('click', function () {
    if (TRANSLATE_BTN.innerHTML.includes('🌐')) {
        const formData = new FormData();
        const headers = new Headers();
        formData.append('txt', ARTICLE_TXT_ELEM.innerHTML);
        formData.append('title', ARTICLE_TITLE_ELEM.textContent);
        fetch('/translate/', {
            method: 'POST',
            headers: headers,
            body: formData
        }).then(response => response.json()).then(data => {
            ARTICLE_TXT_ELEM.innerHTML = data.txt_translation;
            ARTICLE_TITLE_ELEM.textContent = data.title_translation;
        });
        TRANSLATE_BTN.innerHTML = '❌';
    } else {
        window.location.reload();
    }

});