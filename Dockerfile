FROM golang:1.21-alpine AS builder

# Install Python in the Go image
RUN apk add --no-cache python3

WORKDIR /app

# Copy Go module files
COPY go.mod ./
RUN go mod download

# Copy source code
COPY . .

# Build the Go application
RUN go build -o discretelog-server .

# Production stage - use minimal image with both Go binary and Python
FROM alpine:latest

# Install Python3
RUN apk add --no-cache python3

WORKDIR /root/

# Copy the built binary and Python script
COPY --from=builder /app/discretelog-server .
COPY --from=builder /app/pohlig_hellman.py .

EXPOSE 8080

CMD ["./discretelog-server"]