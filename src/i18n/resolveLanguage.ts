export enum LocaleEnum {
  SimplifiedChinese = "zh-Hans",
  TraditionalChinese = "zh-Hant",
  English = "en-US",
  German = "de",
  Korean = "ko",
  Japanese = "ja",
  French = "fr",
  Russian = "ru",
  Italian = "it",
  Arabic = "ar",
  Spanish = "es",
}

const LANGUAGE_ALIASES: Record<string, LocaleEnum> = {
  "zh-cn": LocaleEnum.SimplifiedChinese,
  "zh-hans": LocaleEnum.SimplifiedChinese,
  zh: LocaleEnum.SimplifiedChinese,
  "zh-sg": LocaleEnum.SimplifiedChinese,
  "zh-tw": LocaleEnum.TraditionalChinese,
  "zh-hant": LocaleEnum.TraditionalChinese,
  "zh-hk": LocaleEnum.TraditionalChinese,
  "zh-mo": LocaleEnum.TraditionalChinese,
  en: LocaleEnum.English,
  "en-us": LocaleEnum.English,
  "en-gb": LocaleEnum.English,
  "en-au": LocaleEnum.English,
};

const availableLanguages = Object.values(LocaleEnum);

export function matchLocale(value: string): LocaleEnum {
  const lower = value.toLowerCase();
  const aliased = LANGUAGE_ALIASES[lower];
  if (aliased) {
    return aliased;
  }

  const exact = availableLanguages.find((lang) => lang.toLowerCase() === lower);
  if (exact) {
    return exact;
  }

  const prefix = availableLanguages.find((lang) =>
    lower.startsWith(lang.toLowerCase())
  );
  if (prefix) {
    return prefix;
  }

  const base = lower.split("-")[0];
  return LANGUAGE_ALIASES[base] ?? LocaleEnum.English;
}

export function resolveLanguage(
  pref?: string | null,
  systemLanguage?: string | null
): LocaleEnum {
  const system =
    systemLanguage ||
    (typeof navigator !== "undefined" ? navigator.language : LocaleEnum.English);

  if (!pref || pref === "system") {
    return matchLocale(system);
  }
  return matchLocale(pref);
}
