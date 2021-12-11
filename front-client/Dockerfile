  FROM node:14-slim

  WORKDIR /user/src/app

  COPY ./package.json ./

  COPY ./yarn.lock ./

  RUN npm cache clean --force
  #RUN npm install
  #RUN npm install -D react-scripts
  RUN npm install
 
  COPY . .
  
  EXPOSE 3000
  ENTRYPOINT [ "npm" ]

  CMD ["start"]
