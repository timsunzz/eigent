import log from 'electron-log'
import { getMainWindow } from "../init";

export function canSendToWindow(win?: {
  isDestroyed?: () => boolean;
  webContents?: { isDestroyed?: () => boolean; send: (...args: any[]) => void };
} | null): boolean {
  if (!win) return false;
  if (typeof win.isDestroyed === 'function' && win.isDestroyed()) return false;
  if (win.webContents && typeof win.webContents.isDestroyed === 'function' && win.webContents.isDestroyed()) {
    return false;
  }
  return true;
}

/**
 * Safely send message to main window if it exists and is not destroyed
 * @param channel - The IPC channel to send message to
 * @param data - The data to send
 */
function safeMainWindowSend(channel: string, data?: any) {
  const mainWindow = getMainWindow();
  if (canSendToWindow(mainWindow)) {
    try {
      mainWindow.webContents.send(channel, data);
      return true;
    } catch (error) {
      log.warn(`[WEBCONTENTS SEND] Failed to send ${channel}:`, error);
      return false;
    }
  } else {
    log.warn(`[WEBCONTENTS SEND] Cannot send message to main window: ${channel}`, data);
    return false;
  }
}

export {safeMainWindowSend}