export function resolveApiBase(desktop: { apiBase: string } | undefined, configured: string): string {
  return desktop?.apiBase || configured
}
