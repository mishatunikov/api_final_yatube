# api_final
Данное api реализует возможности "блога", позволяя делиться своими историями или мыслями. 

## Описание 

Функционал:
- Возможность добавлять, редактировать, удалять посты.
- Возможность оставлять комментарии к постам, редактировать и удалять комментарии.
- Возможность подписываться на обновления другого пользователя.


## Установка и запуск

Для корректной работы данного API рекомендуется использовать **Python 3.9.13**.

Для установки проекта выполните следующие шаги:

1. Клонировать репозиторий:
```
https://github.com/mishatunikov/api_final_yatube.git
```
2. Создать и активировать виртуальное окружение:

    Создать:
    - macOS/Linux
    `python -m venv venv`

    - Windows
    `python -m venv venv`

    Активировать:
    - macOS/Linux
    `source venv/bin/activate`

    - Windows
    `source venv\Scripts\activate`


3. Установить зависимости:
```
pip install -r requirements.txt
```
    

4. Применить миграции базы данных: 
```
python manage.py migrate
```
    

5. Запустить сервер разработки:
```
python manage.py runserver
```

## Доступные эндпоинты

Для просмотра **_документации_** API используйте эндпоинт `redoc/`.


### Эндпоинты взаимодействия с API:
1. Модель Post:
   - `api/v1/post/` - поддерживает GET и POST
   - `api/v1/post/<pk:int>/` - поддерживает GET, POST, DELETE, PUT, PATCH

2. Модель Comment:
   - `api/v1/post/<pk:int>/comments/` - поддерживает GET и POST
   - `api/v1/post/<pk:int>/comments/<pk:int>/` - поддерживает GET, POST, DELETE, PUT, PATCH

3. Модель Group:
   - `api/v1/groups/` - поддерживает GET

4. Модель Follow:
   - `api/v1/post/follow/` - поддерживает GET и POST

5. Работа с токенами:
    - `api/v1/jwt/create/` - поддерживает POST
    - `api/v1/jwt/refresh/` - поддерживает POST
    - `api/v1/jwt/verify/`- поддерживает POST

