from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy.orm import sessionmaker

from bot.commands import StateForm
from bot.commands.parse_and_search import get_recept


async def random_recept(message: types.Message, state: FSMContext):
    await message.answer(
        'random_recept'
    )
    await state.set_state(StateForm.GET_BUTTON)


async def recept_with_param(message: types.Message, state: FSMContext):
    await message.answer(
        'Напишите названия продуктов, которые у Вас есть.\nЧерез запятую.'
    )
    await state.set_state(StateForm.GET_PRODUCT)


async def users_product(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
):
    menu_builder = ReplyKeyboardBuilder()

    menu_builder.row(
        KeyboardButton(
            text='Случайный рецепт'
        ),
        KeyboardButton(
            text='Рецепт из имеющегося'
        )
    )

    print(await get_recept(
        session_maker=session_maker,
        link=message.text),
    )

    await message.answer(
        "Рецепт",
        reply_markup=menu_builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(StateForm.GET_BUTTON)

    # list_ingredients = convert_in_list(message.text)
    # list_ingredients_id = []
    # list_recept_id = []

    # response_ingredient_id = await search_ingredient_id(
    #     session_maker=session_maker,
    #     list_ingredient_name=list_ingredients
    # )

    # for ingredient_id in response_ingredient_id:
    #     list_ingredients_id.append(ingredient_id)

    # response_recept_id = await search_recept_id(
    #     session_maker=session_maker,
    #     # list_ingredient_id=list_ingredients_id
    #     list_ingredient_id=[11, 14, 17]
    # )
    #
    # for recept_id in response_recept_id:
    #     for r_id in recept_id:
    #         list_recept_id.append(r_id)
    #
    # response_full_recept = await search_full_recept(
    #     session_maker=session_maker,
    #     recept_id=list_recept_id[0]
    # )
    #
    # get_recept_for_user(response_full_recept)
    # print(get_recept_for_user(response_full_recept))

# def convert_in_list(text: str):
#     data = text.split(",")
#     ingredient_list = []
#     for ingredient in data:
#         ingredient_list.append(ingredient.strip())
#
#     return ingredient_list


# def get_recept_for_user(response_full_recept):
#     recept_name = ""
#     ingredients_with_amount = []
#     for row in response_full_recept:
#         recept_name = f"{row[0]}\n"
#         ingredients_with_amount.append(f"{row[1]} - {row[2]} {row[3]}\n")
#     recept = recept_name + ''.join(ingredients_with_amount)
#     return recept


# def my_lemmatization(text):
#     doc = Doc(text=text)
#     emb = NewsEmbedding()
#     morph_tagger = NewsMorphTagger(emb)
#     segment = Segmenter()
#     morph_vocab = MorphVocab()
#
#     doc.segment(segment)
#     doc.tag_morph(morph_tagger)
#     token_list = []
#     for token in doc.tokens:
#         token.lemmatize(morph_vocab)
#     for token in doc.tokens:
#         token_list.append(token.lemma)
#     return token_list
#
#
# async def search_ingredient_id(
#         session_maker: sessionmaker,
#         list_ingredient_name
# ):
#     async with session_maker() as session:
#         async with session.begin():
#             list_ingredient_id = []
#             for ingredient_name in list_ingredient_name:
#                 stmt = select(Ingredient.ingredient_id).where(Ingredient.ingredient_name == ingredient_name)
#                 result = await session.execute(stmt)
#                 ingredient = result.scalar_one_or_none()
#                 if ingredient:
#                     list_ingredient_id.append(ingredient)
#
#             return list_ingredient_id
#
#
# async def search_recept_id(session_maker: sessionmaker, list_ingredient_id):
#     async with session_maker() as session:
#         async with session.begin():
#             recepts_table = Recept.__table__
#             recepts = aliased(recepts_table, name='r')
#             intermediates_table = Intermediate.__table__
#             intermediates = aliased(intermediates_table, name='i')
#
#             stmt = select(recepts.c.recept_id). \
#                 select_from(
#                 join(recepts, intermediates,
#                      recepts.c.recept_id == intermediates.c.recept_id)). \
#                 where(intermediates.c.ingredient_id.in_(list_ingredient_id)). \
#                 group_by(recepts.c.recept_id, recepts.c.recept_name). \
#                 having(
#                 func.count(intermediates.c.ingredient_id.distinct()) == len(list_ingredient_id),
#                 func.count(intermediates.c.ingredient_id.distinct()) ==
#                 func.count('*')
#             )
#
#             result = await session.execute(stmt)
#             return result.fetchall()
#
#
# async def search_full_recept(
#         session_maker: sessionmaker,
#         recept_id: int
# ):
#     async with session_maker() as session:
#         async with session.begin():
#             intermediate_table = Intermediate.__table__
#             receipts_table = Recept.__table__
#             units_table = Units.__table__
#             ingredients_table = Ingredient.__table__
#             i = aliased(intermediate_table)
#             r = aliased(receipts_table)
#             u = aliased(units_table)
#             i2 = aliased(ingredients_table)
#
#             stmt = select(
#                 r.c.recept_name,
#                 r.c.preparation,
#                 i2.c.ingredient_name,
#                 i.c.amount,
#                 u.c.unit_name
#             ).select_from(
#                 join(
#                     i, r, r.c.recept_id == i.c.recept_id
#                 ).join(
#                     u, u.c.unit_id == i.c.unit_id
#                 ).join(
#                     i2, i2.c.ingredient_id == i.c.ingredient_id
#                 )
#             ).where(
#                 r.c.recept_id == recept_id
#             )
#
#             # Execute the query
#             result = await session.execute(stmt)
#         return result.fetchall()
