(function(){
  const CANON = "760-454-1860";
  const TEL = "+17604541860";

  function enforce() {
    document.querySelectorAll('a[href]').forEach(a => {
      if (a.href.startsWith('tel:') || a.href.startsWith('sms:')) {
        a.href = 'tel:' + TEL;
        if (a.textContent.match(/\d{3}[- ]?\d{3}[- ]?\d{4}/)) {
          a.textContent = CANON;
        }
      }
    });

    document.querySelectorAll('*').forEach(el => {
      if (el.children.length === 0 && el.textContent) {
        el.textContent = el.textContent.replace(/\+?1?\D?760\D?454\D?1860/g, CANON);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enforce);
  } else {
    enforce();
  }
})();
