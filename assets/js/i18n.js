// i18n.js — Shared language switching for yiyol.com
(function () {
  const SUPPORTED_LANGS = ['ko', 'en'];
  const STORAGE_KEY = 'preferredLanguage';
  const LANG_LABELS = { ko: '한국어', en: 'English' };

  function detectBrowserLanguage() {
    const browserLang = (navigator.language || navigator.userLanguage || '').toLowerCase();
    if (browserLang.startsWith('ko')) return 'ko';
    return 'en';
  }

  function getPreferredLanguage() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && SUPPORTED_LANGS.includes(saved)) return saved;
    return detectBrowserLanguage();
  }

  function setLanguage(lang) {
    if (!SUPPORTED_LANGS.includes(lang)) lang = 'en';
    document.documentElement.setAttribute('lang', lang);
    localStorage.setItem(STORAGE_KEY, lang);

    // Update lang-switch UI if present
    var langCurrent = document.querySelector('.lang-current');
    if (langCurrent) {
      langCurrent.textContent = LANG_LABELS[lang];
    }

    document.querySelectorAll('.lang-option').forEach(function (option) {
      if (option.dataset.lang === lang) {
        option.classList.add('active');
      } else {
        option.classList.remove('active');
      }
    });

    var langSwitch = document.querySelector('.lang-switch');
    if (langSwitch) langSwitch.classList.remove('active');
  }

  function initLanguageSwitcher() {
    var langSelector = document.querySelector('.lang-selector');
    var langSwitch = document.querySelector('.lang-switch');

    if (langSelector && langSwitch) {
      langSelector.addEventListener('click', function (e) {
        e.preventDefault();
        langSwitch.classList.toggle('active');
      });

      document.addEventListener('click', function (e) {
        if (!langSwitch.contains(e.target)) {
          langSwitch.classList.remove('active');
        }
      });
    }

    document.querySelectorAll('.lang-option').forEach(function (option) {
      option.addEventListener('click', function (e) {
        e.preventDefault();
        setLanguage(option.dataset.lang);
      });
    });
  }

  // Initialize on DOM ready
  var lang = getPreferredLanguage();
  setLanguage(lang);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLanguageSwitcher);
  } else {
    initLanguageSwitcher();
  }

  // Expose globally
  window.setLanguage = setLanguage;
})();
