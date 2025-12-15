/** @type {import('next').NextConfig} */
const nextConfig = {
  i18n: {
    locales: ['ar', 'he', 'en'],
    defaultLocale: 'ar',
    localeDetection: false
  }
};

module.exports = nextConfig;
