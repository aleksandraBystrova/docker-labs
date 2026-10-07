FROM node:18 AS react-build

WORKDIR /app

COPY client/package*.json ./
RUN npm ci

COPY client/ ./
RUN npm run build


FROM node:18-alpine

WORKDIR /app

COPY --from=react-build /app/build ./build

COPY server/package*.json ./
RUN npm ci --omit=dev

COPY server/server.js ./server.js

USER node

EXPOSE 3000

CMD ["node", "server.js"]
