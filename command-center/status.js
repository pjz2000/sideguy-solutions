(function(){
  const el = document.getElementById("status");
  if(!el) return;
  const now = new Date();
  el.innerHTML =
    "🟢 Command Center Online<br>" +
    "San Diego, CA<br>" +
    now.toLocaleString();
})();
