# Запуск приложения TravelDiary

- Откройте консоль cmd и перейдите в папку с проектом

```
cd ...\TravelDiary
```

- Создайте виртуальное окружение

```
py -m venv .venv
```

- Активируйте виртуальное окружение

```
.venv\Scripts\activate
```

- Установите необходимые библиотеки

```
pip install -r requirements.txt
```

- Выполните миграции

```
python manage.py migrate
```

- Заполните БД тестовыми данными

```
python manage.py loaddata demo_data
```

- Запустите приложение

```
python manage.py runserver
```

- Перейдите по ссылке

```
localhost:8000
```