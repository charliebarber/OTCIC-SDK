FROM node:19-alpine

WORKDIR /api

COPY package*.json /api
COPY /src ./api/src

RUN npm ci --prod

CMD ["node", "api/src/app.js"]