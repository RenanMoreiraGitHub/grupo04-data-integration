FROM node:16

WORKDIR /code

COPY Site .

WORKDIR /code/Site

EXPOSE 3000

RUN npm i
CMD npm start
