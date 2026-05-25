import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#00a884',
        dark: {
          bg: '#111b21',
          header: '#1f2c33',
          panel: '#202c33',
          chat: '#0b141a',
          input: '#2a3942',
          hover: '#2a3942',
        }
      }
    },
  },
  plugins: [],
}
module.exports = config
