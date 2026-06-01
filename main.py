from aiogram import Bot, Dispatcher, Router, F

import random

import os

import json

from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery

from aiogram.filters import Command

from pet import *

import asyncio





safe_pets = "safe_pets.json"


bot = Bot(os.environ["BOT_TOKEN"])

dp = Dispatcher()



battles = {}

router = Router()





ikb =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Тренироваться", callback_data="train")],
    [InlineKeyboardButton(text = "Лечиться", callback_data="heal")],
    [InlineKeyboardButton(text = "Восполнить энергию", callback_data="energy")]

])

ikb_battle = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Согласен", callback_data="yes")],
    [InlineKeyboardButton(text = "Несогласен", callback_data="no")]

])


def safe():
    data = {}
    for user_id, current_pet in pets.items():
        data[str(user_id)] = current_pet.to_dict()

    with open(safe_pets, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load():
    if os.path.getsize(safe_pets) == 0:
        return {}

    with open(safe_pets, "r", encoding="utf-8") as file:
        data = json.load(file)

    load_pets = {}
    for user_id, current_pet in data.items():
        load_pets[int(user_id)] = pet.from_dict(current_pet)
    return load_pets

pets: dict[int, pet] = load()



def get_pet(user_id: int) -> pet | None:
    return pets.get(user_id)

def battle(attacker_pet, defender_pet):
    while(attacker_pet.hp > 0 or defender_pet.hp > 0):
        defender_pet.hp -= attacker_pet.power
        attacker_pet.hp -= defender_pet.power

@router.message(Command("start"))
async def start(message:Message):
    user_id = message.from_user.id

    pets[user_id] = pet()
    safe()
    await message.answer("Питомец создан")
    await message.answer('Выбери действие', reply_markup=ikb)

@router.message(Command("pet"))
async def pet_create(message: Message):
    user_id = message.from_user.id
    current_pet = get_pet(user_id)
    current_pet.update_energy()
    await message.answer(
        f"name: {current_pet.name}\n"
        f"xp: {current_pet.ex}\n"
        f"power: {current_pet.power}\n"
        f"hp: {current_pet.hp}\n"
        f"energy: {current_pet.energy}\n"
    )

@router.message(Command('duel'))
async def fight(message:Message):
    attack_id = message.from_user.id
    if message.reply_to_message is None:
        await message.answer(
            'Нажмите на ответ по сообщению кому вы хотите кинуть дуэль'
        )
        return
    defender_id = message.reply_to_message.from_user.id
    attack_pet = get_pet(attack_id)
    defender_pet = get_pet(defender_id)

    if defender_id == message.bot.id:
        await message.answer(
            f"{attack_id}, Хорошая попытка"
        )
        return

    if defender_id == attack_id:
        await message.answer(
            f"{message.from_user.id}, Победил"
        )
        return

    duel_battle = 1
    battles[duel_battle] = {'attacker_id': attack_id, 'defender_id':defender_id}
    await message.answer(
        'Вас вызывают на дуэль', reply_markup=ikb_battle
    )

@router.callback_query(F.data == "train")
async def pet_train(callback: CallbackQuery):
    user_id = callback.from_user.id
    current_pet = get_pet(user_id)
    current_pet.upgrade()
    safe()
    await callback.answer("Успешно")

@router.callback_query(F.data == "no")
async def no_duel(callback: CallbackQuery):
    await callback.message.answer(
        'откосил от дуэли'
    )


@router.callback_query(F.data == "yes")
async def yes_duel(callback: CallbackQuery):
    battle = battles.get(1)
    attacker_id = battle['attacker_id']
    defender_id = battle['defender_id']
    attacker_pet = get_pet(attacker_id)
    defender_pet = get_pet(defender_id)
    if callback.from_user.id!= defender_id:
        await callback.message.answer("За него не решай")
        return
    await callback.message.answer(
        'начало битвы'
    )
    while (attacker_pet.hp > 0 or defender_pet.hp > 0):
        defender_pet.hp -= attacker_pet.power
        attacker_pet.hp -= defender_pet.power
        await callback.message.answer("раунд закончен")

    if attacker_pet.hp <= 0:
        await callback.message.answer(
            "Победил защищающийся"
        )
    if defender_pet.hp <= 0:
        await callback.message.answer(
            "Победил атакующий"
        )

    safe()




@router.callback_query(F.data == "heal")
async def pet_heal(callback: CallbackQuery):
    user_id = callback.from_user.id
    current_pet = get_pet(user_id)
    current_pet.heal()
    safe()
    await callback.answer("Успешно")



dp.include_router(router)

async def main():
    await dp.start_polling(bot)





asyncio.run(main())
