# polygon.io-api-test

Приложение предназначено для тестирование REST API ресурса polygon.io

Выгружает статистические данные о торгах с помощью обращения к API.
Символы для выгрузки:   MSFT, COST, EBAY, WMT, GOOGL

Предоставляет простой веб интерфейс:
1. Позволяет выбрать параметры построения графика (символ, временной промежуток, параметры запроса к API)
2. Отображает свечной график

При этом данные загружаются в локальную базу данных и догружаются в случае необходимости. 

<h1>Инструкция по установке</h1>

<ol>
  <li><b>git clone https://github.com/max-belichenko/polygon.io-api-test.git</b></li>
<li><b>cd polygon.io-api-test</b></li>
<li><b>python -m venv venv</b>		# python3 -m venv venv</li>
<li><b>venv\Scripts\activate</b>	# source venv/bin/activate	## for Linux</li>
<li><b>pip install -r requirements.txt</b>	# pip3 install -r requirements.txt</li>
<li><b>cd stock_charts</b></li>
<li><b>python manage.py makemigrations</b> # python3 manage.py makemigrations</li>
<li><b>python manage.py migrate</b>  # python3 manage.py migrate</li>
<li><b>python manage.py runserver</b>  # python3 manage.py runserver</li>
</ol>
