FROM node:18-apline

WORKDIR /app

RUN add -D appuser
USER appuser

COPY package*.json ./
RUN npm install

COPY . .

HEALTHCHECK CMD wget --spider http://localhost:3000 || exit 1

CMD ["npm", "start"]