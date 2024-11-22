# RestFS
`Microservice using fastapi and sqlalchemy libs`

Тестовое задание [ГК Эксперт](https://www.prizma72.ru/)

## Задача:
Написать приложение (микросервис) на Python с использованием библиотек [FastAPI](https://fastapi.tiangolo.com/) и [SQLAlchemy](https://www.sqlalchemy.org/).\
Приложение должно реализовать возможность через **REST** интерфейс работать с хранилищем файлов.\
Сами файлы размещаются в файловой системе.\
Информация о файлах находится в базе данных [SQLite](https://www.sqlite.org/) в таблице files.\
В **REST** интерфейсе должен быть реализован полный набор операций **CRUD**.

### Структура таблицы files:

- `id`: integer, not null, autoincrement, primary key – первичный ключ
- `fname`: string, not null – имя файла
- `fsize`: integer, not null – размер файла
- `mdt`: datetime, not null – дата и время модификации файла

### Дополнительные условия:
1. Полная информация о тайминге выполнения задания
2. Программа должна быть написана на [Python 3.8](https://www.python.org/downloads/release/python-3810/)
3. [FastAPI](https://fastapi.tiangolo.com/) и [SQLAlchemy](https://www.sqlalchemy.org/) в синхронном режиме

---

Автор: [Mikhail Kopochinskiy](https://github.com/linkoffee)
