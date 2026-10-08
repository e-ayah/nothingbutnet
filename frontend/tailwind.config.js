/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}",
    "./screens/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
  ],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        primary: "#1a1a2e",
        accent: "#4a4a8a",
        success: "#2d8a2d",
        warning: "#cc6600",
        background: "#f8f8ff",
        white: "#ffffff"
      },
    },
  },
  plugins: [],
};
