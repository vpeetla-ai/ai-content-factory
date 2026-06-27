/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        bg: "#070710",
        surface: "#0E0E1A",
        panel: "#12121F",
        accent: "#7C6FFF",
        teal: "#00E5C3",
        muted: "#5A5A80",
      },
    },
  },
  plugins: [],
};
