# Website Discrete Log Calculator

Microservice API for solving discrete logarithm problems using the Pohlig-Hellman algorithm.

## 🚀 Deployment

- **Status**: Containerized microservice
- **Container Image**: `ghcr.io/qiumatthew/website-discretelog:latest`
- **Tech Stack**: Go HTTP server + Python3 cryptographic algorithms

## 📚 API

### Calculate Discrete Logarithm
```
GET /discrete-log?g={generator}&h={element}&p={modulus}
```

**Parameters:**
- `g`: Generator of the group (integer)
- `h`: Target element (integer) 
- `p`: Prime modulus (integer)

**Returns:** The discrete logarithm k such that g^k ≡ h (mod p)

### Health Check
```
GET /health
```

**Returns:** Service status in JSON format

## 🔧 Development

### Local Testing
```bash
go run main.go
# Server starts on port 8080
```

### Build Container
```bash
./build.sh
```

## 🧮 Algorithm

Uses the **Pohlig-Hellman algorithm** with optimizations:
- Prime factorization by trial division
- Baby-step giant-step for small subgroups
- Chinese Remainder Theorem for combining results
- Time complexity: O(∑ eᵢ × (log n + √qᵢ))

## 🐳 Container Details

Multi-stage Docker build:
1. **Builder stage**: Go 1.21 + Python3 for compilation
2. **Runtime stage**: Minimal Alpine Linux with Python3
3. **Size**: ~50MB production image

## 🔒 Security

- CORS enabled for cross-origin requests
- Input validation for all parameters
- No persistent data storage
- Stateless design