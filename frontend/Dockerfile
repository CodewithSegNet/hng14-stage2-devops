FROM node:18-alpine

WORKDIR /app

RUN addgroup -S appuser && adduser -S appuser -G appuser
USER appuser

COPY package*.json ./
RUN npm install

COPY . .

HEALTHCHECK CMD wget --spider http://localhost:3000 || exit 1

CMD ["npm", "start"]