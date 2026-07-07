/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        bg: "#f4f6fb",
        surface: "#ffffff",
        panel: "#ffffff",
        accent: "#2563eb",
        teal: "#0d9488",
        muted: "#64748b",
        border: "#e2e8f0",
        ink: "#0f172a",
      },
      boxShadow: {
        card: "0 1px 3px rgba(15,23,42,.06), 0 4px 16px rgba(15,23,42,.06)",
      },
    },
  },
  plugins: [],
};
