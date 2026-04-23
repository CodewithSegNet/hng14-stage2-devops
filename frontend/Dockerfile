FROM node:18-alpine

WORKDIR /app

# create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY package*.json ./
RUN npm install

COPY . .

USER appuser

HEALTHCHECK CMD wget -qO- http://localhost:3000 || exit 1

CMD ["npm", "start"]