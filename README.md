# polygon.io-api-test

Приложение предназначено для тестирование REST API ресурса polygon.io

Выгружает статистические данные о торгах с помощью обращения к API.
Символы для выгрузки:   MSFT, COST, EBAY, WMT, GOOGL

Предоставляет простой веб интерфейс:
1. Позволяет выбрать параметры построения графика (символ, временной промежуток, параметры запроса к API)
2. Отображает свечной график

При этом данные загружаются в локальную базу данных и догружаются в случае необходимости. 

<h1>Инструкция по установке</h1>

git clone https://github.com/max-belichenko/polygon.io-api-test.git
cd polygon.io-api-test
python -m venv venv		# python3 -m venv venv
venv\Scripts\activate	# source venv/bin/activate	## for Linux
pip install -r requirements.txt	# pip3 install -r requirements.txt
cd stock_charts
python manage.py makemigrations # python3 manage.py makemigrations
python manage.py migrate  # python3 manage.py migrate
python manage.py runserver  # python3 manage.py runserver
