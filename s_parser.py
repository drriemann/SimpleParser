import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

links_products = []
for i in range(1, 11):
    print(i)
    url = f"https://www.parsemachine.com/sandbox/catalog/?page={i}"
    r = requests.get(url)
    sleep(1.5)
    soup = BeautifulSoup(r.text, 'lxml')

    page_products = soup.findAll('div', class_='col-xl-3 col-lg-3 col-md-4 col-sm-6 col-6 mb-3')
    for product in page_products:
        link = 'https://www.parsemachine.com' + product.find('a', class_="no-hover").get('href')
        links_products.append(link)


data = []
for link in links_products:
    r = requests.get(link)
    # print(link)
    soup = BeautifulSoup(r.text, 'lxml')
    name = soup.find('h1', id="product_name").text.strip()
    price = ' '.join(soup.find('big', id="product_amount").text.strip().split('\xa0'))
    char = '*'.join(soup.find('table', class_="table table-hover mb-2").text.split()[1::3])

    data.append([name, price, char])

header = ['product_name', 'product_amount', 'characteristics']
df = pd.DataFrame(data, columns=header)
with open('res.csv', 'w') as f:
    df.to_csv(f, sep=',', encoding='utf8')
