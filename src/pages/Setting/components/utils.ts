export function parseArgsToArray(args: string): string[] {
  try {
    // Try parsing as JSON array first
    const arr = JSON.parse(args);
    if (Array.isArray(arr)) return arr.map(String);
  } catch { }
  
  // Handle malformed JSON by manually trimming { } and trying again
  if (args.trim().startsWith('{') && args.trim().endsWith('}')) {
    const trimmed = args.trim().slice(1, -1); // Remove { }
    try {
      // Try parsing the trimmed version as JSON array
      const arr = JSON.parse(`[${trimmed}]`);
      if (Array.isArray(arr)) return arr.map(String);
    } catch { }
    
    // If still fails, treat as comma-separated
    if (trimmed.trim()) {
      return trimmed.split(',').map(arg => arg.trim()).filter(arg => arg !== '');
    }
  }
  
  // If not JSON, treat as comma-separated string
  if (args.trim()) {
    return args.split(',').map(arg => arg.trim()).filter(arg => arg !== '');
  }
  
  return [];
}

export function arrayToArgsJson(arr: string[]): string {
  const filtered = arr.filter(v => v.trim() !== '');
  if (filtered.length === 0) return '';
  
  // Return as JSON stringified array
  return JSON.stringify(filtered);
}

/**
 * Provider rows historically used the misspelled `is_vaild` enum (1/2)
 * while the UI sent a boolean `is_valid`. Treat either as configured.
 */
export function isProviderConfigured(provider: {
  is_valid?: boolean | string | number | null;
  is_vaild?: boolean | string | number | null;
} | null | undefined): boolean {
  if (!provider) return false;
  const values = [provider.is_valid, provider.is_vaild];
  return values.some((value) =>
    value === true ||
    value === 2 ||
    value === "2" ||
    value === "is_valid"
  );
}