# ML_business_project
### Предсказание цены акций Норильского Никеля
Стек:

ML: sklearn, pandas, numpy, catboost
API: flask 
Данные: парсинг из открытых источников

Задача: определение справедливой цены акции "Норильского Никеля" по переданному набору данных

Используемые признаки:
USD: float64       
Commitments Long-Term: float64       
Commitments Short-Term: float64       
Earnings per share: float64       
EBITDA: float64       
CB rate: float64       
FRS rate: float64       
Nickel close price, USD: float64       
Copper close price, USD: float64       
Palladium close price, USD: float64       
Platinum close price, USD: float64       
MMVB close: float64   

Модель: CatBoostRegressor

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/zhukovnikolay/ML_business_project.git
$ cd ML_business_project
$ docker build -t zhukovnikolay/ml_business_project .
```

### Запускаем контейнер

```
$ docker run -d -p 8180:8180 zhukovnikolay/ml_business_project
```

### Проверяем работу файлом predict_api_test.ipynb (необходимо предварительно скопировать его и файл test.xlsx на локальную машину)
