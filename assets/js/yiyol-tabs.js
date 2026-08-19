// yiyol-tabs.js — sub-navigation tab switching + scroll-fade (shared across pages)
(function () {
  // ── Sub-nav tabs ──────────────────────────────────────────────
  function activateTab(key) {
    var tabs = document.querySelectorAll('.sv-subnav-tab');
    var panels = document.querySelectorAll('.sv-tabpanel');
    var matched = false;
    tabs.forEach(function (t) {
      var on = t.dataset.tab === key;
      t.classList.toggle('active', on);
      if (on) matched = true;
    });
    panels.forEach(function (p) {
      p.classList.toggle('active', p.dataset.tab === key);
    });
    return matched;
  }

  function initTabs() {
    var tabs = document.querySelectorAll('.sv-subnav-tab');
    if (!tabs.length) return;

    tabs.forEach(function (t) {
      t.addEventListener('click', function () {
        var key = t.dataset.tab;
        activateTab(key);
        if (history.replaceState) {
          history.replaceState(null, '', '#' + key);
        }
      });
    });

    // Activate from hash, else first tab
    var hash = (location.hash || '').replace('#', '');
    if (!hash || !activateTab(hash)) {
      activateTab(tabs[0].dataset.tab);
    }
  }

  // ── Scroll fade-in ────────────────────────────────────────────
  function initFade() {
    var els = document.querySelectorAll('.sv-fade');
    if (!els.length) return;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) entry.target.classList.add('visible');
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
    els.forEach(function (el) { observer.observe(el); });
  }

  function init() { initTabs(); initFade(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
