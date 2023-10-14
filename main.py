import os
import requests




# получение вакансий с HH
url2 = 'https://api.hh.ru/vacancies'
res = requests.get(url2, headers={'User-Agent': 'slon'}, params={'per_page': 4, 'text': 'python'})
print(res.json())
