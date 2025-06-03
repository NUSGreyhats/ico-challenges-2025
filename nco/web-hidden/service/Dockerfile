FROM php:8-apache

COPY www /var/www/html
COPY website.conf /etc/apache2/sites-available/000-default.conf

RUN chmod 777 /var/www/html/admin/uploads
COPY Dockerfile /

ENV FLAG=NCO{hidden_flag_hehe}

EXPOSE 80