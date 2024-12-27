const theme = (() => {
  if (localStorage.getItem("theme")) {
    return localStorage.getItem("theme");
  }
  if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    return "dark";
  }
  return "light";
})();

// Toggling the dark mode class on the body has been inlined to <head>
// to avoid FOUC.
//
// TODO Implement a progressively-enhanced dark mode with CSS as well

window.localStorage.setItem("theme", theme);

const handleToggleClick = () => {
  const element = document.documentElement;
  element.classList.toggle("dark");

  const isDark = element.classList.contains("dark");
  localStorage.setItem("theme", isDark ? "dark" : "light");
};

document
    .getElementById("theme-switcher")
    .addEventListener("click", handleToggleClick);