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

from bot.commands import StateForm


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


async def users_product(message: types.Message, state: FSMContext):
    lemma = await my_lemmatization(message.text)
    result_str = ' '.join(lemma)
    menu_builder = ReplyKeyboardBuilder()

    menu_builder.row(
        KeyboardButton(
            text='Случайный рецепт'
        ),
        KeyboardButton(
            text='Рецепт из имеющегося'
        )
    )

    await message.answer(
        f'{result_str}',
        reply_markup=menu_builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(StateForm.GET_BUTTON)


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
