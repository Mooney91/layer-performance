FROM node:18

WORKDIR /server

COPY package*.json .

RUN npm install

COPY . .

EXPOSE 1337

CMD ["node", "app.js"]