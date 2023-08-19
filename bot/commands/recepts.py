from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from natasha import MorphVocab, Segmenter, NewsMorphTagger, NewsEmbedding, Doc
from sqlalchemy import select, join, desc, func, asc
from sqlalchemy.orm import sessionmaker, aliased

from bot.commands import StateForm
from bot.commands.differ import get_cool_id
from bot.commands.functions import show_unsub_text
from bot.db import Units, Ingredient, Intermediate, Recept, User

another_using = 'Если Вы хотите использовать бота - выберите кнопку.'


async def recept_with_param(message: types.Message, state: FSMContext):
    if User.is_sub_user:
        await message.answer(
            'Напишите названия продуктов, которые у Вас есть.\nЧерез запятую.'
        )
        await state.set_state(StateForm.GET_PRODUCT)
    else:
        await show_unsub_text(
            message=message
        )


async def users_product(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
):
    if User.is_sub_user:
        not_founded_ing = 'Пока что в базе отсутствует ингредиент, который Вы написали.'
        not_founded_rec = 'Пока что в базе отсутствует рецепт, состоящий Ваших из ингредиентов.'

        menu_builder = ReplyKeyboardBuilder()

        menu_builder.row(
            KeyboardButton(
                text='Рецепт из имеющегося'
            )
        )
        list_ingredients = convert_in_list(message.text)
        list_recept_id = []

        response_ingredient_id = await search_ingredient_id(
            session_maker=session_maker,
            list_ingredient_name=list_ingredients
        )

        if response_ingredient_id:
            response_recept_id = await get_intermediate_id(
                session_maker=session_maker,
                list_ingredient_id=response_ingredient_id
            )

            for recept_id in response_recept_id:
                for r_id in recept_id:
                    list_recept_id.append(int(r_id))

            if response_recept_id:
                first_col = await get_recept_inter_id(
                    session_maker=session_maker,
                    list_intermediate_recept_id=list_recept_id
                )

                first = convert_in_int(list_=first_col)

                second_col = await get_another_recept_id(
                    session_maker=session_maker,
                    first_col=first,
                    list_ingredient_id=list_recept_id
                )

                second = convert_in_int(list_=second_col)

                cool_id = get_cool_id(
                    first=first,
                    second=second
                )

                recept = await search_full_recept(
                    session_maker=session_maker,
                    recept_id=cool_id
                )

                await message.answer(
                    get_recept_for_user(recept)
                )
                await message.answer(
                    another_using,
                    reply_markup=menu_builder.as_markup(resize_keyboard=True)
                )
                await state.set_state(StateForm.GET_BUTTON)
            elif not response_recept_id:
                await message.answer(
                    not_founded_rec,
                    reply_markup=menu_builder.as_markup(resize_keyboard=True)
                )
                await state.set_state(StateForm.GET_PRODUCT)
        elif not response_ingredient_id:
            await message.answer(
                not_founded_ing,
                reply_markup=menu_builder.as_markup(resize_keyboard=True)
            )
            await state.set_state(StateForm.GET_PRODUCT)
    else:
        await show_unsub_text(
            message=message
        )

    # for page in range(300):
    #     for link in asd(page_link=f'{message.text}{page+1}'):
    #         await get_recept(link=link, session_maker=session_maker)
    #         print(f'str #{page+1}')


def convert_in_int(list_):
    my_list = [int(row[0]) for row in list_]
    return my_list


def convert_in_list(text: str):
    data = text.split(",")
    ingredient_list = []
    for ingredient in data:
        ingredient_list.append(ingredient.strip())

    return ingredient_list


def get_recept_for_user(response_full_recept):
    recept_name = ''
    recept_preparation = ''
    ingredients_with_amount = []
    for row in response_full_recept:
        recept_name = f'{row[0]}\n'
        ingredients_with_amount.append(f'{row[2]} - {row[3]} {row[4]}\n')
        recept_preparation = f'{row[1]}'
    recept = recept_name + ''.join(ingredients_with_amount) + recept_preparation
    return recept


def my_lemma(text):
    doc = Doc(text=text)
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    segment = Segmenter()
    morph_vocab = MorphVocab()

    doc.segment(segment)
    doc.tag_morph(morph_tagger)
    token_list = []
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    for token in doc.tokens:
        token_list.append(token.lemma)
    return token_list


async def search_ingredient_id(
        session_maker: sessionmaker,
        list_ingredient_name
):
    async with session_maker() as session:
        async with session.begin():
            list_ingredient_id = []
            ingredients_table = Ingredient.__table__

            i = aliased(ingredients_table)
            for ingredient_name in list_ingredient_name:
                stmt = select(i.c.ingredient_id).where(i.c.ingredient_name.like(ingredient_name))
                result = await session.execute(stmt)
                ingredient = result.scalar_one_or_none()
                if ingredient:
                    list_ingredient_id.append(ingredient)

            return list_ingredient_id


async def get_intermediate_id(session_maker: sessionmaker, list_ingredient_id):
    async with session_maker() as session:
        async with session.begin():
            intermediates_table = Intermediate.__table__
            intermediates = aliased(intermediates_table, name='i')

            stmt = select(intermediates.c.id) \
                .where(intermediates.c.ingredient_id.in_(list_ingredient_id))

            result = await session.execute(stmt)
            return result.fetchall()


async def get_recept_inter_id(session_maker: sessionmaker, list_intermediate_recept_id):
    async with session_maker() as session:
        async with session.begin():
            intermediates_table = Intermediate.__table__
            intermediates = aliased(intermediates_table, name='i')

            stmt = select(intermediates.c.recept_id) \
                .where(intermediates.c.ingredient_id.in_(list_intermediate_recept_id)) \
                .group_by(intermediates.c.recept_id) \
                .order_by(desc(func.count()))

            first_col = await session.execute(stmt)
            return first_col.fetchall()


async def get_another_recept_id(session_maker: sessionmaker, first_col, list_ingredient_id):
    async with session_maker() as session:
        async with session.begin():
            intermediates_table = Intermediate.__table__
            intermediates = aliased(intermediates_table, name='i')

            stmt = select(intermediates.c.recept_id) \
                .where(intermediates.c.recept_id.in_(first_col)) \
                .where(intermediates.c.ingredient_id.in_(list_ingredient_id)) \
                .group_by(intermediates.c.recept_id) \
                .order_by(asc(func.count()))
            second_col = await session.execute(stmt)
            return second_col.fetchall()


async def search_recept_id(session_maker: sessionmaker, list_ingredient_id):
    async with session_maker() as session:
        async with session.begin():
            intermediates_table = Intermediate.__table__
            intermediates = aliased(intermediates_table, name='i')

            stmt = select(intermediates.c.recept_id).where(intermediates.c.ingredient_id.in_(list_ingredient_id)) \
                .group_by(intermediates.c.recept_id)

            result = await session.execute(stmt)
            return result.fetchall()


async def search_full_recept(
        session_maker: sessionmaker,
        recept_id: int
):
    async with session_maker() as session:
        async with session.begin():
            intermediate_table = Intermediate.__table__
            receipts_table = Recept.__table__
            units_table = Units.__table__
            ingredients_table = Ingredient.__table__
            i = aliased(intermediate_table)
            r = aliased(receipts_table)
            u = aliased(units_table)
            i2 = aliased(ingredients_table)

            stmt = select(
                r.c.recept_name,
                r.c.preparation,
                i2.c.ingredient_name,
                i.c.amount,
                u.c.unit_name
            ).select_from(
                join(
                    i, r, r.c.recept_id == i.c.recept_id
                ).join(
                    u, u.c.unit_id == i.c.unit_id
                ).join(
                    i2, i2.c.ingredient_id == i.c.ingredient_id
                )
            ).where(
                r.c.recept_id == recept_id
            )

            result = await session.execute(stmt)
        return result.fetchall()
