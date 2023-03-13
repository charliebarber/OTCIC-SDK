FROM golang:1.20-alpine as builder

WORKDIR /app

COPY go.mod .
COPY go.sum .
RUN go mod download

COPY ./ ./

RUN go build -o /api

EXPOSE 3000
CMD ["/api"]
