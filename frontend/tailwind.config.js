/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Design tokens grounded in a wooded, river-flanked campus feel,
        // not the default cream+terracotta AI-generated look.
        paper: "#EEF1EA",      // cool, slightly green-gray off-white
        ink: "#16211B",        // near-black with a green cast, not pure black
        moss: {
          DEFAULT: "#1F3D2B",  // deep forest green — primary
          light: "#2F5540",
        },
        river: {
          DEFAULT: "#46606B",  // slate blue-gray — secondary
          light: "#6E8790",
        },
        ochre: "#C98A2C",      // warm turmeric accent — used sparingly
        alert: "#B4472A",
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        body: ["Inter", "sans-serif"],
        data: ["IBM Plex Mono", "monospace"],
      },
    },
  },
  plugins: [],
};
