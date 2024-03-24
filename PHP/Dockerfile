# Use the official PHP image
FROM php:7.4-apache

# Install mysqli extension
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

# Copy the PHP script into the container
COPY . /var/www/html/
COPY index.html /usr/local/apache2/htdocs/index.html

RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

RUN a2enmod rewrite

# Restart Apache
CMD ["apache2ctl", "-D", "FOREGROUND"]
