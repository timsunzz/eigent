import { describe, it, expect } from 'vitest'
import { getHttpErrorMessage } from '@/api/http'

describe('getHttpErrorMessage', () => {
  it('prefers application text from local API errors', () => {
    expect(getHttpErrorMessage({ text: 'Account or password error', code: 10 }, 200)).toBe(
      'Account or password error'
    )
  })

  it('reads FastAPI detail strings from HTTP errors', () => {
    expect(getHttpErrorMessage({ detail: 'Project not found or access denied' }, 404)).toBe(
      'Project not found or access denied'
    )
  })

  it('reads the first FastAPI validation detail', () => {
    expect(
      getHttpErrorMessage({ detail: [{ msg: 'Field required', loc: ['body', 'email'] }] }, 422)
    ).toBe('Field required')
  })

  it('falls back to the HTTP status when no body is present', () => {
    expect(getHttpErrorMessage(null, 500)).toBe('Request failed with status 500')
  })
})
