import { describe, expect, it } from "vitest";
import {
  filenameFromUrl,
  getFileExtension,
  normalizeRelativePath,
  safeDecodeURIComponent,
  splitCommandArgs,
} from "../../../../electron/main/utils/pathUtils";

describe("electron pathUtils", () => {
  it("extracts a decoded download filename", () => {
    expect(
      filenameFromUrl("https://cdn.example.com/files/%E4%B8%AD%E6%96%87%20report.pdf")
    ).toBe("中文 report.pdf");
  });

  it("normalizes Windows relative paths", () => {
    expect(normalizeRelativePath("project\\task_1\\docs")).toBe("project/task_1/docs");
  });

  it("parses quoted command arguments", () => {
    expect(splitCommandArgs(`uvx "mcp-remote" --config "/Users/我的 配置/a.json"`)).toEqual([
      "uvx",
      "mcp-remote",
      "--config",
      "/Users/我的 配置/a.json",
    ]);
  });

  it("returns empty extension for names without a suffix", () => {
    expect(getFileExtension("README")).toBe("");
    expect(safeDecodeURIComponent("%")).toBe("%");
  });
});
