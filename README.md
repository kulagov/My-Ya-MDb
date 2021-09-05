# Проект YaMDb
![yamdb_workflow workflow](https://github.com/kulagov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Описание проекта
Проект YaMDb позволяет собирать отзывы и оценку пользователей на произведения. Для произведений предусмотрена разбивка по категориям и жанрам. Список категорий и жанров определяется администратором. Диаппазон оценок от одного до десяти. Для каждого произведения формируется усредненная оценка - рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Адрес - [178.154.223.65]

## Инструкция по запуску
После клонирования репозитория необходимо создать [git secrets]:

 - ALLOWED_HOSTS: разрешенные хосты, по умолчанию "*"
 - DB_ENGINE: django.db.backends.postgresql
 - DB_HOST: db
 - DB_NAME: postgres
 - DB_PORT: 5432
 - DEBUG: False
 - DOCKER_PASSWORD: (пароль от вашего аккаунта в [Docker])
 - DOCKER_USERNAME: (username вашего аккаунта в [Docker])
 - EMAIL_ADMIN: (ваш e-mail)
 - HOST: (публичный адрес вашего сервера)
 - PASSPHRASE: (пароль SHH ключа)
 - POSTGRES_PASSWORD: (пароль доступа к базе данных)
 - POSTGRES_USER: (userame админа базы данных)
 - SECRET_KEY: (secret key django)
 - SSH_KEY: (SSH key для доступа к вашему серверу)
 - TELEGRAM_TO: (id вашего аккаунта в Telegram)
 - TELEGRAM_TOKEN: (token вашего бота в telegram)
 - USER: (username для доступа к серверу)

После чего выполнить push в репозиторий.

Произойдет автоматическое тестирование, сборка образа, загрузка образа в [Docker], закачивание и запуск образа на сервере.

Затем, на сервере применяем миграции, создаем администратора и загружаем начальные данные:

    docker-compose exec web python manage.py migrate --noinput

    docker-compose exec web python manage.py createsuperuser

    docker-compose exec web python manage.py loaddata fixtures.json


## Использованные технологии
[Python 3.7]

[Django 3.0.5]

[Django REST framework 3.11.0]

[Docker]

## Об авторе
[Павел Кулагов]

[Python 3.7]: https://python.org
[Django 3.0.5]: https://www.djangoproject.com/
[Django REST framework 3.11.0]: https://www.django-rest-framework.org/
[Docker]: https://www.docker.com/
[Павел Кулагов]: https://github.com/kulagov
[git secrets]: https://docs.github.com/en/actions/reference/encrypted-secrets
[178.154.223.65]: http://178.154.223.65/