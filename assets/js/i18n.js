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

  // 언어별 URL 이 따로 있는 페이지(/en/blog/ 등)는 <html data-lang-fixed> 로 언어가 고정된다.
  var FIXED_LANG = document.documentElement.getAttribute('data-lang-fixed');

  // hreflang 대체 링크가 있으면 언어 전환은 그 URL 로 이동한다.
  function alternatePath(lang) {
    var link = document.querySelector('link[rel="alternate"][hreflang="' + lang + '"]');
    if (!link) return null;
    try { return new URL(link.getAttribute('href'), location.href).pathname; } catch (e) { return null; }
  }

  function getPreferredLanguage() {
    if (FIXED_LANG && SUPPORTED_LANGS.includes(FIXED_LANG)) return FIXED_LANG;
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && SUPPORTED_LANGS.includes(saved)) return saved;
    return detectBrowserLanguage();
  }

  function setLanguage(lang) {
    if (!SUPPORTED_LANGS.includes(lang)) lang = 'en';
    document.documentElement.setAttribute('lang', lang);
    // 언어가 고정된 페이지는 열어 보는 것만으로 방문자의 언어 선택을 바꾸지 않는다.
    if (!FIXED_LANG) localStorage.setItem(STORAGE_KEY, lang);

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

    // 블로그는 언어별 URL 이 따로 있으므로 링크도 선택한 언어 쪽으로 돌린다.
    if (!FIXED_LANG) {
      document.querySelectorAll('a[href^="/blog/"], a[href^="/en/blog/"]').forEach(function (a) {
        var path = a.getAttribute('href').replace(/^\/en\/blog\//, '/blog/');
        a.setAttribute('href', lang === 'en' ? '/en' + path : path);
      });
    }
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
        var lang = option.dataset.lang;
        var path = alternatePath(lang);
        if (path && path !== location.pathname) {
          localStorage.setItem(STORAGE_KEY, lang);
          location.href = path + location.hash;
          return;
        }
        setLanguage(lang);
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

  // ── Mobile hamburger menu ────────────────────────────────────────────────
  var ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>';
  var ICON_CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>';

  function injectHamburger(rootSelector, innerSelector) {
    document.querySelectorAll(rootSelector).forEach(function (root) {
      var inner = root.querySelector(innerSelector);
      if (!inner || inner.querySelector('.nav-hamburger')) return;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'nav-hamburger';
      btn.setAttribute('aria-label', 'Toggle navigation menu');
      btn.setAttribute('aria-expanded', 'false');
      btn.innerHTML = ICON_MENU;
      inner.appendChild(btn);
      btn.addEventListener('click', function () {
        var open = root.classList.toggle('is-mobile-open');
        btn.setAttribute('aria-expanded', String(open));
        btn.innerHTML = open ? ICON_CLOSE : ICON_MENU;
      });
      // Auto-close when a menu link is tapped
      root.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () {
          if (root.classList.contains('is-mobile-open')) {
            root.classList.remove('is-mobile-open');
            btn.setAttribute('aria-expanded', 'false');
            btn.innerHTML = ICON_MENU;
          }
        });
      });
    });
  }

  function initMobileNav() {
    injectHamburger('.site-nav', '.site-nav-inner');
    injectHamburger('header.header', '.nav');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileNav);
  } else {
    initMobileNav();
  }
})();
