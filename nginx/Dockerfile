FROM nginx:latest
RUN mkdir -p /app/staticfiles
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/html/index.html /usr/share/nginx/html/index.html
EXPOSE 80