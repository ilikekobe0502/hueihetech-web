/* Google Ads 轉換追蹤：載入 gtag 並在點擊商店連結時回報「點擊商店按鈕」轉換 */
(function () {
  var ADS_ID = 'AW-18528346658';
  var STORE_CLICK_LABEL = 'vyl1CL2957odEKLEgINF';

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ADS_ID;
  document.head.appendChild(s);

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', ADS_ID);

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a') : null;
    if (!a) return;
    var h = a.href || '';
    if (h.indexOf('play.google.com') > -1 || h.indexOf('apps.apple.com') > -1) {
      gtag('event', 'conversion', {
        send_to: ADS_ID + '/' + STORE_CLICK_LABEL,
        transport_type: 'beacon'
      });
    }
  }, true);
})();
