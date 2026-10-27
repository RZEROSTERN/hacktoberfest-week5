import { resolveApiBase } from '../utils/api'

export function useApi() {
  const config = useRuntimeConfig()
  const baseURL = resolveApiBase(window.desktop, config.public.apiBase)
  return $fetch.create({ baseURL })
}
