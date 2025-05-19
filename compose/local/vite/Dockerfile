FROM docker.io/node:22.14-bookworm-slim

WORKDIR /app

COPY ./package.json ./pnpm-lock.yaml /app/

RUN corepack enable && corepack prepare pnpm@latest --activate \
  && pnpm install --frozen-lockfile \
  && pnpm store prune \
  && pnpm cache clean

ENV PATH=./node_modules/.bin/:$PATH
