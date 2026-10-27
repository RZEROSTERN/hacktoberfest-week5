export default defineNuxtConfig({
  compatibilityDate: '2026-10-27',
  ssr: false,
  modules: ['@nuxt/eslint'],
  css: ['~/assets/css/style.css'],
  devtools: { enabled: false },
  telemetry: false,
  typescript: { strict: true },
  runtimeConfig: { public: { apiBase: 'http://127.0.0.1:8765' } },
  app: { head: { title: 'La Última Vela / The Last Candle', htmlAttrs: { lang: 'en' } } },
})
