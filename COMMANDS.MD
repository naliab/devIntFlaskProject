## Миграция моделей в БД

1. Создать папку миграций и файлы инициализации базы данных:

`flask db init`

2. Сгенерировать первую миграцию на основе текущего состояния вашей базы данных:

`flask db migrate`

3. Применить созданную миграцию к вашей базе данных:

`flask db upgrade`

4. Создать супер-пользователя

`flask create_initial_admin`

5. Установить глобальную переменную в БД

`SET GLOBAL LOCAL_INFILE=1`

6. Импортировать данные

`flask load_data`

**Просьба не включать директорию `migrations` в GIT-репозиторий.**

## Замечания при работе с проектом

Для применения изменений на фронте требуется перезапуск проекта.