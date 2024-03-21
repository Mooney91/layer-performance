FROM php:8.2-cli

RUN docker-php-ext-install mysqli

COPY . /usr/src/myapp

WORKDIR /usr/src/myapp

CMD [ "php", "performance.php" ]