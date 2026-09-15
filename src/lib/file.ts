/** File-name helpers used by renderer UI and Electron IPC. */

export function getFileExtension(filename: string | undefined | null): string {
	if (!filename) return "";
	const lastDot = filename.lastIndexOf(".");
	if (lastDot <= 0 || lastDot === filename.length - 1) return "";
	return filename.slice(lastDot + 1).toLowerCase();
}

export function getFileBaseName(filename: string | undefined | null): string {
	if (!filename) return "";
	const lastDot = filename.lastIndexOf(".");
	if (lastDot <= 0) return filename;
	return filename.slice(0, lastDot);
}

export function normalizeRelativePath(relativePath: string | undefined | null): string {
	return (relativePath || "").replaceAll("\\", "/");
}

export function safeDecodeURIComponent(value: string): string {
	try {
		return decodeURIComponent(value);
	} catch {
		return value;
	}
}

/**
 * Split a shell-style command into argv tokens, preserving quoted
 * paths that contain spaces or non-ASCII characters.
 */
export function splitCommandArgs(command: string): string[] {
	const args: string[] = [];
	let current = "";
	let quote: '"' | "'" | null = null;

	for (let i = 0; i < command.length; i++) {
		const ch = command[i];
		if (quote) {
			if (ch === quote) {
				quote = null;
			} else {
				current += ch;
			}
			continue;
		}
		if (ch === '"' || ch === "'") {
			quote = ch;
			continue;
		}
		if (/\s/.test(ch)) {
			if (current) {
				args.push(current);
				current = "";
			}
			continue;
		}
		current += ch;
	}

	if (current) args.push(current);
	return args;
}
