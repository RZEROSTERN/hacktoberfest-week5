export {}

declare global {
  interface Window { desktop?: { readonly apiBase: string } }
}
