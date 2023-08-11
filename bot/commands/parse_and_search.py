import random
from itertools import islice

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

url_list = []

site_for_search = 'nyamkin.ru'

with DDGS() as ddgs:
    ddgs_gen = ddgs.text(f"рецепты состоящие только из +помидоров site:{site_for_search}", backend="lite")
    for r in islice(ddgs_gen, 15):
        url_list.append(r.get('href'))


def qwe(list_url):
    list_ = []
    current_url = random.choice(list_url)
    response = requests.get(current_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.findAll('a')

        for link in links:
            li = link.get('href')

            if li is not None and li.startswith('/recipes'):
                full_link = f'https://{site_for_search}{li}'
                list_.append(full_link)
    else:
        print(response.status_code)
    return list_


def get_link(links_with_recept):
    link_with_recept = random.choice(links_with_recept)
    response = requests.get(link_with_recept)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1', class_='recept-title').text.strip()
        ingredients_with_amounts = []
        ingredient_elements = soup.find_all('div', class_='row produkt-row')
        for ingredient_element in ingredient_elements:
            ingredient_name_element = ingredient_element.find('span', itemprop='recipeIngredient')
            ingredient_amount_element = ingredient_element.find('span', class_='ingr-quantity')
            ingredient_unit_element = ingredient_element.find('span', class_='mera')

            if ingredient_name_element is not None:
                ingredient_name = ingredient_name_element.text.strip()
            else:
                ingredient_name = ''

            if ingredient_amount_element is not None:
                ingredient_amount = ingredient_amount_element.text.strip()
            else:
                ingredient_amount = ''

            if ingredient_unit_element is not None:
                ingredient_unit = ingredient_unit_element.text.strip()
            else:
                ingredient_unit = ''

            ingredients_with_amounts.append((ingredient_name, ingredient_amount, ingredient_unit))

        preparation_steps = []
        step_elements = soup.find_all('div', class_='dicription_step')
        for step_element in step_elements:
            step = step_element.get_text().strip()
            preparation_steps.append(step)

        # Print the extracted data
        print('Recipe Title:', title)
        print('Ingredients with Amounts:')
        for ingredient, amount, unit in ingredients_with_amounts:
            print('-', amount, unit, ingredient)
        print('Preparation Steps:')
        for index, step in enumerate(preparation_steps, start=1):
            print(f'{index}. {step}')


get_link(qwe(url_list))
