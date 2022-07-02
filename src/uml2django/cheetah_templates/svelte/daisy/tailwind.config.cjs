module.exports = {
  content: ['./src/routes/**/*.{svelte,js,ts}','./src/lib/**/*.{svelte,js,ts}'],
  plugins: [require("daisyui")],
  daisyui: {
    styled: true,
    themes: ["corporate","halloween",],
    base: true,
    utils: true,
    logs: true,
    rtl: false,
    prefix: "",
    darkTheme: "halloween",
  },
}