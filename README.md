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

## Инструкция по эксплуатации:
- [Установка](#установка)
- [Запуск](#запуск)
- [Использование](#использование)
  - [Доступные эндпоинты](#доступные-эндпоинты)
  - [Примеры запросов](#примеры-запросов)

### Установка:
1. Склонируйте репозиторий
```console
git clone https://github.com/linkoffee/RestFS.git
cd RestFS
```
2. Создайте виртуальное окружение
```console
py -3.8 -m venv venv
source venv/bin/activate      # Для Linux/MacOS
source venv\Scripts\activate  # Для Windows 
```
3. Установите зависимости
```console
pip install -r requirements.txt
```

### Запуск:
Находясь в корневой директории запустите локальный сервер:
```console
uvicorn app.main:app --reload
```
Сервер будет доступен по адресу: http://127.0.0.1:8000
> [!NOTE]
> После запуска сервера в корне проекта будет автоматически создана папка `storage/`.\
> Здесь и будут находится все созданные файлы.

### Использование:

**Протестировать API можно по адресу:** http://127.0.0.1:8000/docs

#### Доступные эндпоинты
| Метод | Эндпоинт | Описание |
| ----- | -------- | -------- |
| `POST` | `/files/` | Создать новый файл |
| `GET` | `/files/` | Получить список всех файлов |
| `GET` | `/files/{id}` | Получить информацию о файле по ID |
| `PUT` | `/files/{id}` | Обновить данные файла (имя) |
| `DELETE` | `/files/{id}` | Удалить файл по ID |

#### Примеры запросов
1. Создание файла

`REQUEST`
```b
curl -X 'POST' \
  'http://127.0.0.1:8000/files/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "fname": "new-file.txt",
  "content": "Hello, i`m new file ^^"
}'
```
```json
{
  "fname": "new-file.txt",
  "content": "Hello, i`m new file ^^"
}
```
`RESPONSE`
```json
{
  "id": 1,
  "fname": "new-file.txt",
  "fsize": 22,
  "mdt": "2024-11-27T12:50:22.090538",
  "content": "Hello, i`m new file ^^"
}
```

2. Получение списка файлов

`REQUEST`
```b
curl -X 'GET' \
  'http://127.0.0.1:8000/files/' \
  -H 'accept: application/json'
```
`RESPONSE`
```json
[
  {
    "id": 1,
    "fname": "old-file.txt",
    "fsize": 21,
    "mdt": "2009-06-28T21:32:40.251760",
    "content": "Very very old file..."
  },
  {
    "id": 2,
    "fname": "new-file.txt",
    "fsize": 22,
    "mdt": "2024-11-27T12:56:55.008335",
    "content": "Hello, i`m new file ^^"
  }
]
```

3. Обновление файла

`REQUEST`
```b
curl -X 'PUT' \
  'http://127.0.0.1:8000/files/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "fname": "old-file.txt",
  "content": "I was updated for the first time in 15 years!"
}'
```
```json
{
  "fname": "old-file.txt",
  "content": "I was updated for the first time in 15 years!"
}
```
`RESPONSE`
```json
{
  "id": 1,
  "fname": "old-file.txt",
  "fsize": 45,
  "mdt": "2024-11-27T12:59:06.817540",
  "content": "I was updated for the first time in 15 years!"
}
```

4. Удаление файла

`REQUEST`
```b
curl -X 'DELETE' \
  'http://127.0.0.1:8000/files/1' \
  -H 'accept: application/json'
```
`RESPONSE`
```json
{
  "message": "File №1 was deleted successfully."
}
```

---

Автор: [Mikhail Kopochinskiy](https://github.com/linkoffee)
