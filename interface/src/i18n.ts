import { createI18n } from 'vue-i18n';
import ptBR from '@/assets/locale/pt-BR.json';
import en from '@/assets/locale/en.json';

const savedLocale = localStorage.getItem('lang') || 'pt-BR';

const i18n = createI18n({
  locale: savedLocale,
  fallbackLocale: 'pt-BR',
  messages: {
    'pt-BR': ptBR,
    'en': en,
  }
});

export default i18n;
