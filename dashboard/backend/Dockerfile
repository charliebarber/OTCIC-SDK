FROM golang:1.20-alpine as builder

WORKDIR /app

COPY go.mod .
COPY go.sum .
RUN go mod download

COPY ./ ./

RUN go build -o /api

FROM alpine:3
COPY --from=builder /api .


CMD ["/api"]
