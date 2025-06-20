FROM golang:1.20 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main main.go

FROM scratch
WORKDIR /root/
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]