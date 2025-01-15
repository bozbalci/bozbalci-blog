// Tailwind v4 beta does not support setting multiple triggers for variant
// TODO Migrate this to main.css when v4 adds support
module.exports = {
  darkMode: [
    "variant",
    [
      "@media (prefers-color-scheme: dark) { &:not(.light *) }",
      "&:is(.dark *)",
    ],
  ],
};
