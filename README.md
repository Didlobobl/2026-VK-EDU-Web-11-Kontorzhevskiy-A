# Проект "AskPupkin" — Сервис вопросов и ответов

Учебный проект в рамках курса VK Education "Web-технологии". Сервис позволяет пользователям задавать вопросы, отвечать на них, голосовать за лучшие решения и формировать сообщество.

## Технологии на данном этапе:
*   **Верстка:** HTML5, CSS3.
*   **Фреймворк:** Bootstrap 5.3, подключенный локально.
*   **Адаптивность:** Реализована сетка для десктопов (>=1200px), планшетов (768px) и мобильных устройств (375px).
* **Контейнеризация:** Docker, docker-compose

## Как запустить верстку:
### Локальный запуск (с виртуальным окружением)

1. Клонируйте репозиторий:  
   `git clone <ссылка_на_ваш_репозиторий>`
2. Перейдите в папку проекта:  
   `cd 2026-VK-EDU-Web-11-Kontorzhevskiy-A`
3. Создайте и активируйте виртуальное окружение:  
   `python -m venv venv`  
   - Windows: `venv\Scripts\activate`  
   - Linux/macOS: `source venv/bin/activate`
4. Установите зависимости:  
   `pip install -r requirements.txt`
5. Выполните миграции:  
   `python manage.py migrate`
6. Запустите сервер:  
   `python manage.py runserver`
7. Откройте в браузере [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Запуск через Docker Compose
1. Убедитесь, что установлены Docker и docker-compose.
2. Из корня проекта выполните:  
   `docker compose up --build`
3. Откройте [http://localhost:8000/](http://localhost:8000/).

## Список страниц и роутов
| Страница | URL | Имя маршрута (для `{% url %}`) |
|----------|-----|-------------------------------|
| Главная (новые вопросы) | `/` | `questions:index` |
| Лучшие вопросы | `/hot/` | `questions:hot` |
| Вопросы по тегу | `/tag/<slug:tag_name>/` | `questions:tag` |
| Страница вопроса | `/question/<int:question_id>/` | `questions:question` |
| Добавить вопрос | `/ask/` | `questions:ask` |
| Вход | `/accounts/login/` | `core:login` |
| Регистрация | `/accounts/signup/` | `core:signup` |
| Настройки профиля | `/accounts/profile/` | `core:profile` |



## Структура проекта
*   `application/` — Настройки Django (settings.py, urls.py).
*   `core/` — Приложение для аутентификации и профиля.
*   `questions/` — Приложение для вопросов и ответов.
*   `templates/` — Общие шаблоны (base.html).
*   `static/` — Собранная статика .
*   `media/` — Загруженные пользователями файлы.
*   `manage.py` — Скрипт управления Django.
*   `requirements.txt` — Зависимости проекта.
*   `.gitignore` — Игнорирование служебных файлов IDE, кэша Python и системного мусора.
*   `.env.example` — Пример переменных окружения.
*   `Dockerfile` — Инструкция для сборки образа.
*   `docker-compose.yml` — Оркестрация контейнеров.
*   `README.md` — Документация.