FROM node:20-alpine
WORKDIR /app

# Shared package
COPY shared/package.json shared/tsconfig.json shared/src ./shared/
RUN cd shared && npm install && npm run build || true

# Web app deps
COPY web/package.json web/package-lock.json* web/yarn.lock* ./web/
RUN cd web && npm install

# Source
COPY shared ./shared
COPY web ./web

WORKDIR /app/web
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

CMD ["npm", "run", "start"]
