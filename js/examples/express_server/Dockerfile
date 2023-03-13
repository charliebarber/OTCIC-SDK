FROM node:19-alpine as builder
# Build the OTCIC package first
WORKDIR /app

# Install yalc to docker
RUN npm install --global --unsafe-perm yalc 

COPY ./otcic /otcic
WORKDIR /otcic
RUN npm install
RUN yalc publish 

COPY ./examples/express_server /express_server
WORKDIR /express_server
RUN yalc add otcic
RUN npm install

CMD ["node", "app.js"]
