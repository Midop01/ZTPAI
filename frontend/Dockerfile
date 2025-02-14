# Stage 1: Build the Svelte app
FROM node:14-alpine as builder
WORKDIR /app
COPY package.json rollup.config.js ./
COPY src ./src
COPY public ./public
RUN npm install
RUN npm run build

# Stage 2: Serve the static files with a lightweight server
FROM node:14-alpine
RUN npm install -g serve
WORKDIR /app
COPY --from=builder /app/public .
EXPOSE 5000
CMD ["serve", "-s", "."]
