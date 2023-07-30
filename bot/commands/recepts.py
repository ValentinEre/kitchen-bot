from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    Doc
)
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot.commands import StateForm
from bot.db import Ingredient


async def random_recept(message: types.Message, state: FSMContext):
    await message.answer(
        'random_recept'
    )
    await state.set_state(StateForm.GET_BUTTON)


async def recept_with_param(message: types.Message, state: FSMContext):
    await message.answer(
        'Напишите названия продуктов, которые у Вас есть.\nЧерез пробел.'
    )
    await state.set_state(StateForm.GET_PRODUCT)


async def users_product(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
):
    # lemma = await my_lemmatization(message.text)
    # result_str = ' '.join(lemma)
    menu_builder = ReplyKeyboardBuilder()

    menu_builder.row(
        KeyboardButton(
            text='Случайный рецепт'
        ),
        KeyboardButton(
            text='Рецепт из имеющегося'
        )
    )

    stmt = await search_in_db(
        session_maker=session_maker,
        query='nuts'
    ),

    await message.answer(
        # f'{result_str}',
        stmt,
        reply_markup=menu_builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(StateForm.GET_BUTTON)


async def search_in_db(
        session_maker: sessionmaker,
        query: str
) -> str:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Ingredient.ingredient_name).where(
                    (Ingredient.ingredient_name == query)
                )
            )
            return sql_res.all()


async def my_lemmatization(text):
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
