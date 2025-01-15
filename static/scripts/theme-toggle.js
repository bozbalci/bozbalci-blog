const themeSelect = document.getElementById("theme-switcher");

themeSelect.value = localStorage.getItem("theme") || "system";

// Toggling the dark mode class on the body has been inlined to <head>
// to avoid FOUC.

const handleThemeChange = (event) => {
  const selectedTheme = event.target.value;

  localStorage.setItem("theme", selectedTheme);

  const element = document.documentElement;
  element.classList.toggle("dark", selectedTheme === "dark");
  element.classList.toggle("light", selectedTheme === "light");

  const isDark =
    selectedTheme === "dark" ||
    (selectedTheme === "system" &&
      matchMedia("(prefers-color-scheme: dark)").matches);
  const metaThemeColor = document.querySelector('meta[name="theme-color"]');
  metaThemeColor.setAttribute("content", isDark ? "#111210" : "#fcfdfc");
};

document
  .getElementById("theme-switcher")
  .addEventListener("change", handleThemeChange);