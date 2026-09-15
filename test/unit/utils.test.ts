// Example unit test for utility functions
import { describe, it, expect } from 'vitest'
import { cn } from '@/lib/utils'
import {
  getFileBaseName,
  getFileExtension,
  normalizeRelativePath,
  safeDecodeURIComponent,
  splitCommandArgs,
} from '@/lib/file'

describe('utils', () => {
  describe('cn function', () => {
    it('should merge class names correctly', () => {
      const result = cn('class1', 'class2')
      expect(result).toBe('class1 class2')
    })

    it('should handle conditional classes', () => {
      const result = cn('base', true && 'conditional', false && 'hidden')
      expect(result).toBe('base conditional')
    })

    it('should handle object-style classes', () => {
      const result = cn('base', {
        'active': true,
        'disabled': false
      })
      expect(result).toBe('base active')
    })

    it('should merge conflicting Tailwind classes correctly', () => {
      // twMerge should handle conflicting classes
      const result = cn('p-2', 'p-4')
      expect(result).toBe('p-4')
    })

    it('should handle empty inputs', () => {
      const result = cn()
      expect(result).toBe('')
    })

    it('should handle null and undefined inputs', () => {
      const result = cn('base', null, undefined, 'valid')
      expect(result).toBe('base valid')
    })

    it('should handle arrays of classes', () => {
      const result = cn(['class1', 'class2'], 'class3')
      expect(result).toBe('class1 class2 class3')
    })
  })

  describe('file helpers', () => {
    it('should take the last extension and keep CJK / spaced names', () => {
      expect(getFileExtension('my.report.pdf')).toBe('pdf')
      expect(getFileExtension('季度 报告.docx')).toBe('docx')
      expect(getFileExtension('no-extension')).toBe('')
      expect(getFileBaseName('my.report.pdf')).toBe('my.report')
      expect(getFileBaseName('季度 报告.docx')).toBe('季度 报告')
    })

    it('should normalize Windows relative paths for the folder tree', () => {
      expect(normalizeRelativePath('task_x\\subdir')).toBe('task_x/subdir')
      expect(normalizeRelativePath('')).toBe('')
    })

    it('should decode URLs without throwing on a literal percent', () => {
      expect(safeDecodeURIComponent('%E4%B8%AD%E6%96%87.pdf')).toBe('中文.pdf')
      expect(safeDecodeURIComponent('100% done')).toBe('100% done')
    })

    it('should keep quoted and CJK arguments intact', () => {
      expect(splitCommandArgs('npx -y "@scope/pkg" --path "/tmp/my file"')).toEqual([
        'npx',
        '-y',
        '@scope/pkg',
        '--path',
        '/tmp/my file',
      ])
      expect(splitCommandArgs('echo 中文 路径')).toEqual(['echo', '中文', '路径'])
    })
  })
})
