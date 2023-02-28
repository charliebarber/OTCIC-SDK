# Build with NPM
FROM node:19 as builder

WORKDIR /dashboard

COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY . ./
RUN npm run build
RUN npm ci --prod

FROM node:19-alpine
COPY package.json ./
COPY package-lock.json ./
COPY --from=builder ./dashboard/node_modules dashboard/node_modules
COPY --from=builder ./dashboard/build dashboard/build

EXPOSE 3000
CMD ["node", "dashboard/build"]