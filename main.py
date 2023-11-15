import asyncio
import logging
import sys
import json
import os

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from config import TOKEN, FILE, menu, division_type, format_settings_menu, cars, ages, sexes, works, countries
from utils import update_user, is_user_completed
from formaters import in_absolute, in_percent
from placers import place_age, place_car, place_sex, place_work, place_country

bot_dispatcher = Dispatcher()


@bot_dispatcher.message(Command('help', 'menu'))
async def menu_handler(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    for menu_item in menu:
        builder.button(text=menu_item, callback_data="menu_"+menu_item)
    builder.adjust(2)
    await message.answer(
        """
        Комманды для ручного ввода:
        \t*/help* или */menu* ➩ Это меню\.
        \t*/start* ➩ Общее меню опроса\.
        \t*/result* ➩ Результаты опроса участников\.
        \t*/settings* ➩ Настройки опросника\.
        """,
        parse_mode=ParseMode.MARKDOWN_V2)
    await message.answer("Или как InlineButtons", reply_markup=builder.as_markup())


@bot_dispatcher.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    for menu_item in menu:
        builder.button(text=menu_item, callback_data="menu_"+menu_item)
    builder.adjust(2)
    await message.answer(f"Привет, *{message.from_user.first_name}*\!\nЯ бот опросник и я могу _провести опрос_ и _показать общие результаты_ опросов других\. \nТакже ты можешь _настроить тип и формат_ выводимой информации\.", reply_markup=builder.as_markup(),  parse_mode=ParseMode.MARKDOWN_V2)


@bot_dispatcher.callback_query(F.data == "menu_"+menu[0])
async def your_age_handler(callback: types.CallbackQuery) -> None:
    builder = ReplyKeyboardBuilder()
    for age in ages:
        builder.add(types.KeyboardButton(text=age))
    builder.adjust(1)
    await callback.message.answer("Твой возраст? ", reply_markup=builder.as_markup())


@bot_dispatcher.message(F.text.startswith('от') | F.text.contains('до'))
async def your_country_handler(message: Message) -> None:
    user_values = {
            "user_id": message.from_user.id,
            "age": message.text,
            "country": None,
            "sex": None,
            "work": None,
            "car": None,
            "is_complete": False,
    }
    with open(f"user_{message.from_user.id}.json", "w", encoding="utf-8") as file:
        json.dump(user_values, file)

    builder = ReplyKeyboardBuilder()
    for contry in countries:
        builder.add(types.KeyboardButton(text=f"|{contry['emoji']} {contry['name']}|"))
    builder.adjust(5)

    await message.answer("Твоя страна? ", reply_markup=builder.as_markup(one_time_keyboard=True))


@bot_dispatcher.message(F.text.startswith('|') | F.text.endswith('|'))
async def your_sex_handler(message: Message) -> None:
    start_pos = message.text.find(' ') + 1
    await update_user(message.from_user.id, 'country', message.text[start_pos:])

    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="♂ Мужчина"))
    builder.add(types.KeyboardButton(text="♀ Женщина"))
    await message.answer("Твой пол? ", reply_markup=builder.as_markup(one_time_keyboard=True))


@bot_dispatcher.message(F.text.startswith('♂') | F.text.startswith('♀'))
async def your_work_handler(message: Message) -> None:
    start_pos = message.text.find(' ') + 1
    await update_user(message.from_user.id, 'sex', message.text[start_pos:])

    builder = InlineKeyboardBuilder()
    for work in works:
        builder.button(text=work, callback_data="work_" + work)
    builder.adjust(3)

    await message.answer(
            "Где работаешь, то есть, какая сфера ?",
            reply_markup=builder.as_markup(one_time_keyboard=True)
    )


@bot_dispatcher.callback_query(F.data.startswith("work_"))
async def your_car_handler(callback: types.CallbackQuery) -> None:
    start_pos = callback.data.find('_') + 1
    await update_user(callback.from_user.id, 'work', callback.data[start_pos:])

    builder = ReplyKeyboardBuilder()
    for car in cars:
        builder.add(types.KeyboardButton(text=car))
    await callback.message.answer("Есть ли у тебя машина ?", reply_markup=builder.as_markup(one_time_keyboard=True))


@bot_dispatcher.message(F.text.contains("машин"))
async def end_quiz_handler(message: Message) -> None:
    await update_user(message.from_user.id, 'car', message.text)

    if await is_user_completed(message.from_user.id):
        with open(f"user_{message.from_user.id}.json", "r",  encoding="utf-8") as file:
            user_values = json.load(file)
        if not os.path.exists(FILE):
            with open(FILE, "a", encoding="utf-8") as file:
                file.write("[]")
        with open(FILE, "r", encoding="utf-8") as file:
            users = json.load(file)
            users.append(user_values)
        with open(FILE, "w", encoding="utf-8") as file:
            json.dump(users, file)

    os.remove(f"user_{message.from_user.id}.json")

    builder = InlineKeyboardBuilder()
    builder.button(text="Результат", callback_data="menu_" + menu[1])
    await message.answer("Опрос закончен.\nСпасибо за участие.")
    await message.answer("Теперь можно посмотреть на результат.", reply_markup=builder.as_markup())


@bot_dispatcher.callback_query(F.data == "menu_"+menu[2])
async def setting_callback(callback: types.CallbackQuery):
    await setting(callback.message)


@bot_dispatcher.message(Command("settings"))
async def setting_command(message: Message) -> None:
    await setting(message)


@bot_dispatcher.callback_query(F.data.contains("format_setting_"))
async def setting_update_format_numbers(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    for set_menu in format_settings_menu:
        if set_menu in callback.data:
            builder.button(text="+ " + set_menu, callback_data="format_setting_"+set_menu)
            global division_type
            division_type = set_menu
        else:
            builder.button(text=set_menu, callback_data="format_setting_"+set_menu)
    builder.adjust(2)
    await callback.bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=builder.as_markup())


@bot_dispatcher.message(Command("result"))
async def result_command_handler(message: Message) -> None:
    await result(message)


@bot_dispatcher.callback_query(F.data == "menu_"+menu[1])
async def result_callback_handler(callback: types.CallbackQuery) -> None:
    await result(callback.message)


async def setting(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    for set_menu in format_settings_menu:
        builder.button(text=set_menu, callback_data="format_setting_"+set_menu)
    builder.adjust(2)
    await message.answer("Настройки формата", reply_markup=builder.as_markup())


async def result(message: Message) -> None:
    if not os.path.exists(FILE):
        builder = InlineKeyboardBuilder()
        builder.button(text="Начать", callback_data="menu_" + menu[0])
        await message.answer("Извини, база данных пуста. Пройди опрос первым !", reply_markup=builder.as_markup())
        return

    with open(FILE, "r", encoding="utf-8") as file:
        users = json.load(file)
    with open("result_template.md", "r", encoding="utf-8") as file:
        template = file.read()
    # Define result output
    result = template.replace("divisiontype", division_type)
    # Result output in absolute numbers
    if division_type == format_settings_menu[0]:
        result = place_age(result, users, in_absolute)
        result = place_country(result, users, in_absolute)
        result = place_sex(result, users, in_absolute)
        result = place_work(result, users, in_absolute)
        result = place_car(result, users, in_absolute)
    else:
        result = place_age(result, users, in_percent)
        result = place_country(result, users, in_percent)
        result = place_sex(result, users, in_percent)
        result = place_work(result, users, in_percent)
        result = place_car(result, users, in_percent)

    await message.answer(result, parse_mode=ParseMode.MARKDOWN_V2)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot_dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
