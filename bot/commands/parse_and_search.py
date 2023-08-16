from typing import Any

import requests
from bs4 import BeautifulSoup
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, aliased

from bot.db import Ingredient, Units, Recept, Intermediate

url_list = []


def asd(page_link):
    site_for_search = 'nyamkin.ru'
    list_ = []
    response = requests.get(page_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.findAll('a')

        for link in links:
            li = link.get('href')

            if li is not None and li.startswith('/recipes'):
                full_link = f'https://{site_for_search}{li}'
                if full_link not in list_:
                    list_.append(full_link)

    else:
        print(response.status_code)
    return list_


async def get_recept(
        link,
        session_maker: sessionmaker
):
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1', class_='recept-title').text.strip()
        ingredients_with_amounts = []
        ingredient_elements = soup.find_all('div', class_='row produkt-row')
        for ingredient_element in ingredient_elements:
            ingredient_name_element = ingredient_element.find('span', itemprop='recipeIngredient')
            ingredient_amount_element = ingredient_element.find('span', class_='ingr-quantity')
            ingredient_unit_element = ingredient_element.find('div', class_="col-sm-4 col-xs-3 mera")

            if ingredient_name_element is not None:
                ingredient_name = ingredient_name_element.text.strip()
            else:
                ingredient_name = ''

            if ingredient_amount_element is not None:
                ingredient_amount = ingredient_amount_element.text.strip()
            else:
                ingredient_amount = ''

            if ingredient_unit_element is not None:
                ingredient_unit = ingredient_unit_element.contents[3].text.strip()
            else:
                ingredient_unit = ''

            ingredients_with_amounts.append((ingredient_name, ingredient_amount, ingredient_unit))

        preparation_steps = []
        step_elements = soup.find_all('div', class_='dicription_step')
        for step_element in step_elements:
            step = step_element.get_text().strip()
            preparation_steps.append(step)

        # recipe_info = f"Рецепт: {title}\nИнгредиенты:"
        # for ingredient, amount, unit in ingredients_with_amounts:
        #     recipe_info += f"\n- {amount} {unit} {ingredient}"
        # recipe_info += "\nПриготовление:"
        # for index, step in enumerate(preparation_steps, start=1):
        #     recipe_info += f"\n{index}. {step}"

        await add_title(
            session_maker=session_maker,
            title=title,
            preparation_steps=preparation_steps
        )

        await add_ingredients_and_units(
            ingredients_with_amounts=ingredients_with_amounts,
            session_maker=session_maker
        )
        id_and_amount = await get_id_and_amount(
            title=title,
            ingredients_with_amounts=ingredients_with_amounts,
            session_maker=session_maker
        )

        await qwe(
            id_and_amount=id_and_amount,
            session_maker=session_maker
        )


async def add_title(
        session_maker: sessionmaker,
        title,
        preparation_steps
):
    preparation = ''
    for index, step in enumerate(preparation_steps, start=1):
        preparation += f"\n{index}. {step}"
    async with session_maker() as session:
        async with session.begin():
            recept = Recept(recept_name=title, preparation=preparation)

            session.add(recept)
            await session.commit()


async def add_ingredients_and_units(
        session_maker: sessionmaker,
        ingredients_with_amounts
):
    for ingredient, amount, unit in ingredients_with_amounts:
        async with session_maker() as session:
            async with session.begin():
                existing_ingredient = await check_ingredient(session_maker=session_maker, ingredient=ingredient)
                existing_unit = await check_unit(session_maker=session_maker, unit=unit)

                if not existing_ingredient:
                    ing = Ingredient(ingredient_name=ingredient)
                    session.add(ing)

                if not existing_unit:
                    un = Units(unit_name=unit)
                    session.add(un)
                await session.commit()


async def check_ingredient(
        session_maker: sessionmaker,
        ingredient
):
    async with session_maker() as session:
        async with session.begin():
            ingredients_table = Ingredient.__table__

            i = aliased(ingredients_table)
            stmt_select_ing = select(i).where(i.c.ingredient_name == ingredient)
            result = await session.execute(stmt_select_ing)
            existing_ing = result.scalar_one_or_none()
            return existing_ing is not None


async def check_unit(
        session_maker: sessionmaker,
        unit
):
    async with session_maker() as session:
        async with session.begin():
            units_table = Units.__table__
            u = aliased(units_table)
            stmt_select_unit = select(u).where(u.c.unit_name == unit)
            result = await session.execute(stmt_select_unit)
            existing_unit = result.scalar_one_or_none()
            return existing_unit is not None


async def get_id_and_amount(
        title,
        ingredients_with_amounts,
        session_maker: sessionmaker,
) -> list[tuple[Any, Any, Any, Any]]:
    list_id_and_amount = []
    receipts_table = Recept.__table__
    units_table = Units.__table__
    ingredients_table = Ingredient.__table__
    r = aliased(receipts_table)
    u = aliased(units_table)
    i = aliased(ingredients_table)

    async with session_maker() as session:
        async with session.begin():
            for ingredient, amount, unit in ingredients_with_amounts:
                stmt_t = select(r.c.recept_id).where(r.c.recept_name == title)
                stmt_i = select(i.c.ingredient_id).where(i.c.ingredient_name == ingredient)
                stmt_u = select(u.c.unit_id).where(u.c.unit_name == unit)
                result_t = await session.execute(stmt_t)
                result_i = await session.execute(stmt_i)
                result_u = await session.execute(stmt_u)
                recept_id = result_t.scalar_one_or_none()
                ingredient_id = result_i.scalar_one_or_none()
                unit_id = result_u.scalar_one_or_none()
                list_id_and_amount.append((recept_id, ingredient_id, amount, unit_id))
    return list_id_and_amount


async def qwe(
        id_and_amount,
        session_maker
):
    for recept_id, ingredient_id, amount, unit_id in id_and_amount:
        if amount == '':
            amount = 0
        await add_intermediate(
            session_maker=session_maker,
            recept_id=recept_id,
            ingredient_id=ingredient_id,
            amount=float(amount),
            unit_id=unit_id
        )


async def add_intermediate(
        session_maker: sessionmaker,
        recept_id,
        ingredient_id,
        amount,
        unit_id,
):
    async with session_maker() as session:
        async with session.begin():
            intermediate = Intermediate(
                recept_id=recept_id,
                ingredient_id=ingredient_id,
                amount=amount,
                unit_id=unit_id
            )
            session.add(intermediate)
        await session.commit()
