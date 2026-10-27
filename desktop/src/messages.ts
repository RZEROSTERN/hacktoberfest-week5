const en = {
  title: 'The Last Candle',
  errorTitle: 'The candle could not be lit',
  errorBody: 'A local game service could not start. Close the game and try again. If this continues, reinstall the application.',
}
const es: typeof en = {
  title: 'La Última Vela',
  errorTitle: 'No pudimos encender la vela',
  errorBody: 'No se pudo iniciar un servicio local del juego. Cierra el juego e inténtalo de nuevo. Si el problema continúa, reinstala la aplicación.',
}
export function messages(locale: string): typeof en { return locale.startsWith('es') ? es : en }
