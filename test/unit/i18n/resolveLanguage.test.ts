import { describe, expect, it } from 'vitest'
import { LocaleEnum, matchLocale, resolveLanguage } from '@/i18n/resolveLanguage'

describe('matchLocale', () => {
  it('maps persisted Simplified Chinese after toLowerCase()', () => {
    expect(matchLocale('zh-Hans')).toBe(LocaleEnum.SimplifiedChinese)
    expect(matchLocale('zh-hans')).toBe(LocaleEnum.SimplifiedChinese)
    expect(matchLocale('zh-CN')).toBe(LocaleEnum.SimplifiedChinese)
  })

  it('maps traditional Chinese aliases', () => {
    expect(matchLocale('zh-Hant')).toBe(LocaleEnum.TraditionalChinese)
    expect(matchLocale('zh-TW')).toBe(LocaleEnum.TraditionalChinese)
  })

  it('matches available languages case-insensitively', () => {
    expect(matchLocale('en-us')).toBe(LocaleEnum.English)
    expect(matchLocale('DE')).toBe(LocaleEnum.German)
    expect(matchLocale('ja-JP')).toBe(LocaleEnum.Japanese)
  })
})

describe('resolveLanguage', () => {
  it('uses system locale when preference is system or empty', () => {
    expect(resolveLanguage('system', 'zh-CN')).toBe(LocaleEnum.SimplifiedChinese)
    expect(resolveLanguage('', 'de-DE')).toBe(LocaleEnum.German)
    expect(resolveLanguage(undefined, 'en-US')).toBe(LocaleEnum.English)
  })

  it('applies an explicit saved language', () => {
    expect(resolveLanguage('zh-Hans', 'en-US')).toBe(LocaleEnum.SimplifiedChinese)
  })
})
