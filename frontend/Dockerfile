# Stage 1: Install dependencies
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

# Stage 2: Runtime
FROM node:18-alpine AS runtime

WORKDIR /app

# create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# copy dependencies from builder
COPY --from=builder /app/node_modules ./node_modules

COPY --chown=appuser:appgroup . .

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3000/ || exit 1

CMD ["node", "app.js"]