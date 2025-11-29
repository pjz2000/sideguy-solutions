document.querySelectorAll('[data-include]').forEach(async (element) => {
  const file = element.getAttribute('data-include');
  const resp = await fetch(file);
  element.innerHTML = await resp.text();
});
