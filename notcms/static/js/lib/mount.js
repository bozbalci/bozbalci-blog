export default function mount(selector, callback) {
  window.addEventListener('load', () => {
    const element = document.querySelector(selector);
    if (element) {
      console.log(element);
      callback(element);
    }
  });
}
