export default function mount(selector, callback) {
  window.addEventListener('load', () => {
    document.querySelectorAll(selector).forEach(callback);
  });
}
