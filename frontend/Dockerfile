FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* tsconfig.json vite.config.ts vitest.config.ts ./
RUN npm install --silent --no-progress || (if [ -f package-lock.json ]; then exit 1; else npm install --package-lock-only --silent --no-progress; fi)
COPY index.html ./
COPY src ./src
RUN npm run build
CMD ["npm", "run", "preview"]
