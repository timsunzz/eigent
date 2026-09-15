import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import { resources } from "./locales";
import { getAuthStore, useAuthStore } from "@/store/authStore";
import { LocaleEnum, resolveLanguage } from "./resolveLanguage";

export { LocaleEnum, resolveLanguage } from "./resolveLanguage";

function applyLanguageFromStore() {
  const resolved = resolveLanguage(getAuthStore().language);
  if (i18n.language !== resolved) {
    void i18n.changeLanguage(resolved);
  }
}

i18n.use(initReactI18next).init({
  resources,
  fallbackLng: LocaleEnum.English,
  lng: resolveLanguage(getAuthStore().language),
  interpolation: {
    escapeValue: false,
  },
});

const persistApi = (useAuthStore as { persist?: { onFinishHydration: (cb: () => void) => void; hasHydrated: () => boolean } }).persist;
if (persistApi) {
  persistApi.onFinishHydration(() => {
    applyLanguageFromStore();
  });
  if (persistApi.hasHydrated()) {
    applyLanguageFromStore();
  }
}

export const switchLanguage = (lang: LocaleEnum | "system" | string) => {
  getAuthStore().setLanguage(lang);
  void i18n.changeLanguage(resolveLanguage(lang));
};

export default i18n;
