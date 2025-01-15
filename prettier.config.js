const config = {
  plugins: ["prettier-plugin-jinja-template"],
  overrides: [
    {
      files: ["*.html"],
      options: {
        parser: "jinja-template",
      },
    },
  ],
};

export default config;
