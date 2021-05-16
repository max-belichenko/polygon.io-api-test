# polygon.io-api-test

Приложение предназначено для тестирование REST API ресурса polygon.io

Выгружает статистические данные о торгах с помощью обращения к API.
Символы для выгрузки:   MSFT, COST, EBAY, WMT, GOOGL

Предоставляет простой веб интерфейс:
1. Позволяет выбрать параметры построения графика (символ, временной промежуток, параметры запроса к API)
2. Отображает свечной график

При этом данные загружаются в локальную базу данных и догружаются в случае необходимости. 