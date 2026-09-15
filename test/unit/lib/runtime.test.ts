import { describe, it, expect, afterEach } from 'vitest'
import { getElectronPlatform, isElectronRuntime } from '@/lib'

describe('runtime helpers', () => {
  const originalElectronAPI = window.electronAPI

  afterEach(() => {
    window.electronAPI = originalElectronAPI
  })

  it('detects an Electron runtime when the preload API exists', () => {
    window.electronAPI = { getPlatform: () => 'linux' } as any
    expect(isElectronRuntime()).toBe(true)
    expect(getElectronPlatform()).toBe('linux')
  })

  it('treats a browser / web-only session as non-Electron', () => {
    window.electronAPI = undefined as any
    expect(isElectronRuntime()).toBe(false)
    expect(getElectronPlatform()).toBe('')
  })
})
