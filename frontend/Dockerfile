FROM node:19-alpine3.15 as builder

WORKDIR /app

COPY package.json .
COPY package-lock.json .
RUN npm ci

ARG REACT_APP_PUBLIC_IP="http://localhost:5000/"
ENV REACT_APP_PUBLIC_IP ${REACT_APP_PUBLIC_IP}
COPY . .
RUN npm run build --prod



FROM nginx:1.23.2-alpine

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*
COPY --from=builder /app/build .
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
ENTRYPOINT ["nginx", "-g", "daemon off;"]