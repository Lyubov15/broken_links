# Broken Links

 Приложение на Django проверяет HTML-разметки, находит все внутренние и внешние ссылки и проверяет их работоспособность.

## Технологии

- **Python** 
- **Django** 
- **requests** — для HTTP-запросов
- **BeautifulSoup4** — для парсинга HTML
- **SQLite** — база данных 

## Структура проекта

```
broken_links/
├── analyzer/                 # Основное приложение
│   ├── models.py             # Модели Page, Link, Error
│   ├── views.py              # Логика анализа
│   ├── urls.py
│   ├── templates/analyzer/   # Шаблоны (home, analyze, results)
│   └── migrations/
├── seo_tool/                 # Настройки Django-проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── static/                   # CSS-стили
├── manage.py
├── requirements.txt
└── db.sqlite3
```

## Установка и запуск

1. Клонируйте репозиторий

   ```bash
   git clone https://github.com/Lyubov15/broken_links.git
   cd broken_links
   ```

2. Установите зависимости

   ```bash
   pip install -r requirements.txt
   ```

3. Примените миграции

   ```bash
   python manage.py migrate
   ```

4. Запустите сервер разработки

   ```bash
   python manage.py runserver
   ```

5. Откройте в браузере

   ```
   http://127.0.0.1:8000/
   ```

## Использование

1. На главной странице перейдите к анализу.
2. Введите URL (с `http://` / `https://` или без — протокол добавится автоматически).
3. Нажмите **«Анализировать»**.
4. На странице результатов вы увидите:
   - URL и дату проверки.
   - Валидность HTML.
   - Список ошибок (если есть).
   - Таблицу всех найденных ссылок с типом и HTTP-статусом.
