"""
import requests
from bs4 import BeautifulSoup


# Making a GET request
objects = requests.get('https://airef.github.io/tables/objects.html')
techs = requests.get('https://airef.github.io/tables/techs.html')

soup = BeautifulSoup(objects.text, features="html.parser")

#x = soup.find("table",attrs={"class":"objects-table"}).text.strip()
#x = soup.body.find('th', attrs={'class' : 'objects-ainame-col'}).text
x = soup.body.find("div",attrs={'class' : 'container'}).text
#x = soup.body.find("table").text
print(x)
"""