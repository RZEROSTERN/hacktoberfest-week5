import fs from 'node:fs'
import path from 'node:path'
import { app, BrowserWindow, dialog, protocol } from 'electron'
import { APP_ORIGIN, APP_SCHEME, apiEnv, apiUrl, ollamaEnv, ollamaUrl } from './env'
import { dataDirs, layout } from './layout'
import { reapOrphans } from './pidfile'
import { twoFreePorts } from './ports'
import { sweepPrograms } from './processes'
import { serve } from './protocol'
import { isAllowedRequest, isAppUrl } from './security'
import { Service, Supervisor } from './supervisor'
import { messages } from './messages'

protocol.registerSchemesAsPrivileged([
  { scheme: APP_SCHEME, privileges: { standard: true, secure: true, supportFetchAPI: true, corsEnabled: true } },
])

const supervisor = new Supervisor()
let stopping = false
let stopped = false
let window: BrowserWindow | null = null
let programsDir: string | undefined

async function start(): Promise<void> {
  const text = messages(app.getLocale())
  const dirs = dataDirs(app.getPath('userData'))
  for (const dir of Object.values(dirs)) fs.mkdirSync(dir, { recursive: true })
  const pidFile = path.join(dirs.data, 'services.json')
  await reapOrphans(pidFile)
  const [ollama, api] = await twoFreePorts()
  const ports = { ollama, api }
  const paths = layout(app.isPackaged ? process.resourcesPath : path.join(__dirname, '..', 'build'))
  if (!app.isPackaged) paths.webRoot = path.resolve(__dirname, '..', '..', 'web', '.output', 'public')
  programsDir = paths.programsDir
  const handlers = { onFatal: () => { dialog.showErrorBox(text.errorTitle, text.errorBody); app.quit() } }
  const common = { pidFile, startTimeoutMs: 90_000 }
  await supervisor.startAll([
    new Service({ ...common, name: 'ollama', command: paths.ollamaBinary, args: ['serve'],
      env: ollamaEnv(ports, dirs, process.env), healthUrl: `${ollamaUrl(ports)}/api/tags`,
      logFile: path.join(dirs.data, 'ollama.log') }, handlers),
    new Service({ ...common, name: 'api', command: paths.apiBinary,
      env: apiEnv(ports, dirs, paths, process.pid, process.env), healthUrl: `${apiUrl(ports)}/health`,
      logFile: path.join(dirs.data, 'api.log') }, handlers),
  ])

  const apiOrigin = apiUrl(ports)
  protocol.handle(APP_SCHEME, request => {
    const result = serve(paths.webRoot, request.url, apiOrigin)
    return new Response(new Uint8Array(Buffer.from(result.body)), { status: result.status, headers: result.headers })
  })
  window = new BrowserWindow({
    width: 1280, height: 800, minWidth: 800, minHeight: 600, show: false,
    title: text.title, backgroundColor: '#100f24',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), contextIsolation: true, sandbox: true,
      nodeIntegration: false, webviewTag: false, devTools: !app.isPackaged,
      additionalArguments: [`--last-candle-api-base=${apiOrigin}`],
    },
  })
  window.webContents.on('will-navigate', (event, url) => { if (!isAppUrl(url)) event.preventDefault() })
  window.webContents.setWindowOpenHandler(() => ({ action: 'deny' }))
  const session = window.webContents.session
  session.setPermissionRequestHandler((_contents, _permission, callback) => callback(false))
  session.setPermissionCheckHandler(() => false)
  session.webRequest.onBeforeRequest((details, callback) => {
    callback({ cancel: !isAllowedRequest(details.url, apiOrigin) })
  })
  window.once('ready-to-show', () => window?.show())
  window.on('closed', () => { window = null })
  await window.loadURL(`${APP_ORIGIN}/`)
}

if (!app.requestSingleInstanceLock()) {
  app.quit()
} else {
  app.on('second-instance', () => { window?.restore(); window?.focus() })
  app.on('window-all-closed', () => app.quit())
  app.on('before-quit', event => {
    if (stopped) return
    event.preventDefault()
    if (stopping) return
    stopping = true
    void supervisor.stopAll().finally(() => {
      if (programsDir) sweepPrograms(programsDir)
      stopped = true
      app.quit()
    })
  })
  void app.whenReady().then(start).catch(() => {
    const text = messages(app.getLocale())
    dialog.showErrorBox(text.errorTitle, text.errorBody)
    app.quit()
  })
}
