from cgitb import html
from bs4 import BeautifulSoup
import requests
import html

res = requests.get('https://bank.uz/currency')
html_doc = html.unescape(res.text)


soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.find_all('div', class_='bc-inner-blocks-left'))
