FROM node:20-alpine
WORKDIR /app

# Shared package
COPY shared/package.json shared/tsconfig.json shared/src ./shared/
RUN cd shared && npm install && npm run build || true

# Mobile deps
COPY mobile/package.json mobile/package-lock.json* mobile/yarn.lock* ./mobile/
RUN cd mobile && npm install

COPY shared ./shared
COPY mobile ./mobile

WORKDIR /app/mobile
CMD ["npm", "run", "start"]
