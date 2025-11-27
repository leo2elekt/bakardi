function setLanguage(lang) {
    localStorage.setItem('preferredLanguage', lang);
    applyLanguage(lang);
}

function applyLanguage(lang) {
    document.querySelectorAll('[data-en]').forEach(el => {
        const translation = el.getAttribute(`data-${lang}`);
        if (translation) {
            el.textContent = translation;
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('en-btn').addEventListener('click', () => setLanguage('en'));
    document.getElementById('mk-btn').addEventListener('click', () => setLanguage('mk'));
    document.getElementById('al-btn').addEventListener('click', () => setLanguage('al'));

    const savedLang = localStorage.getItem('preferredLanguage') || 'en';
    applyLanguage(savedLang);
});
