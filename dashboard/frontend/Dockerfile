# Build with NPM
FROM node:19-alpine as builder

WORKDIR /dashboard

COPY package.json ./
COPY package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build
RUN npm prune --production
# RUN npm ci --omit-dev

FROM node:19-alpine
# COPY package.json ./
# COPY package-lock.json ./
COPY --from=builder ./dashboard/node_modules dashboard/node_modules
COPY --from=builder ./dashboard/build dashboard/build
COPY package.json .

EXPOSE 3000
CMD ["node", "dashboard/build"]