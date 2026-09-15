import { describe, expect, it, vi } from 'vitest'

vi.mock('electron-log', () => ({
  default: { warn: vi.fn(), info: vi.fn(), error: vi.fn() },
}))

vi.mock('../../../../electron/main/init', () => ({
  getMainWindow: vi.fn(),
}))

import { canSendToWindow } from '../../../../electron/main/utils/safeWebContentsSend'

describe('canSendToWindow', () => {
  it('rejects missing or destroyed windows', () => {
    expect(canSendToWindow(null)).toBe(false)
    expect(canSendToWindow({
      isDestroyed: () => true,
      webContents: { send: () => undefined },
    })).toBe(false)
  })

  it('rejects destroyed webContents', () => {
    expect(canSendToWindow({
      isDestroyed: () => false,
      webContents: {
        isDestroyed: () => true,
        send: () => undefined,
      },
    })).toBe(false)
  })

  it('accepts a live window', () => {
    expect(canSendToWindow({
      isDestroyed: () => false,
      webContents: {
        isDestroyed: () => false,
        send: () => undefined,
      },
    })).toBe(true)
  })
})
