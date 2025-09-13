from aiogram import Bot, Dispatcher, types
import asyncio
import json
import os

from aiohttp.helpers import TOKEN
from service.database import info_retrieve

# from database import save

bot = Bot(TOKEN)
dp = Dispatcher()
user_data = {}

@dp.message()
async def handle_text(message:types.Message):
    user_id = message.from_user.id
    if user_id not in user_data or message.text == '/start':
        await start(message)
    elif message.text == 'Назад':
        await back(message)
    elif 'lang_dict' not in user_data[user_id]:
        await get_language(message)
        await main_menu(message)
    elif 'state' not in user_data[user_id]:
        await check_menu_buttons(message)
    elif 'vacancy' == user_data[user_id]['state']:
        await fill_form(message)
    elif 'show_cities' == user_data[user_id]['state']:
        await show_vacancy(message)
    elif 'show_vacancies' == user_data[user_id]['state']:
        await choose_branch(message)


    # elif message.text == ''


async def back(message:types.Message):
    print(6, user_data)
    user_id = message.from_user.id
    if user_data[user_id]['state'] == 'vacancy':
        del user_data[user_id]['state']
        await main_menu(message)
    elif user_data[user_id]['state'] == 'fill_form':
        del user_data[user_id]['state']
        await check_menu_buttons(message)
    elif user_data[user_id]['state'] == 'show_cities':
        del user_data[user_id]['state']
        await check_menu_buttons(message)
    elif user_data[user_id]['state'] == 'show_vacancies':
        # del user_data[user_id]['state']
        await fill_form(message)
    elif user_data[user_id]['state'] == 'choose_branch':
        # del user_data[user_id]['state']
        await show_vacancy(message)



async def start(message:types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    info = info_retrieve()
    # save(user_id)
    print(1, user_data)
    photo = types.FSInputFile(path=os.path.join("C:/Users/User/u11_tg_admin/", info[0][3]))
    buttons = [
        [types.KeyboardButton(text='🇷🇺RU'), types.KeyboardButton(text='🇺🇿UZ')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    # await message.answer('Привет! Выберите язык общения:', reply_markup=keyboard)
    await message.answer_photo(photo=photo, caption=info[0][1], reply_markup=keyboard)


async def get_language(message:types.Message):
    user_id = message.from_user.id
    lang = message.text[2:].lower()
    lang_file = open('../ненужное/translate.json', 'r', encoding='UTF-8')
    lang_file = json.load(lang_file)
    lang_dict = lang_file[lang]
    user_data[user_id]['lang_dict'] = lang_dict
    print(2, user_data)



async def main_menu(message:types.Message):
    user_id = message.from_user.id
    buttons = []

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    print(3, user_data)

    await message.answer(user_data[user_id]['lang_dict']['greeting'], reply_markup=keyboard)


async def check_menu_buttons(message:types.Message):
    user_id = message.from_user.id
    user_data[user_id]['state'] = ''

    print(4, user_data)
    if message.text == user_data[user_id]['lang_dict']['vacancy'] or message.text == 'Назад':
        user_data[user_id]['state'] = 'vacancy'
        # video = 'BAACAgIAAxkBAAIi9WhvyA6l7ON0uKFPSq_mOZUtr60yAAJ8dQACNfqAS4h4Cqkji6fTNgQ'
        buttons = [
           [types.KeyboardButton(text="Заполнить анкету")],
           [types.KeyboardButton(text="Назад")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        await message.answer(
                             "Инструкция: Бот задаст вам ряд вопросов, вы должны ввести их все полностью",
                             reply_markup=keyboard)
    # elif...


async def fill_form(message:types.Message):
    user_id = message.from_user.id
    cities = user_data[user_id]['lang_dict']['cities']
    print(5, user_data)
    user_data[user_id]['state'] = 'fill_form'
    if message.text == 'Заполнить анкету' or message.text == 'Назад':
        user_data[user_id]['state'] = 'show_cities'
        buttons = []
        for city in cities:
            buttons.append([types.KeyboardButton(text=city)])
        buttons.append([types.KeyboardButton(text='Главное меню')])
        buttons.append([types.KeyboardButton(text='Назад')])
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        await message.answer("✏️ Давайте приступим к заполнению анкеты для трудоустройства.")
        await message.answer("Выберите регион в котором хотите работать", reply_markup=keyboard)


async def show_vacancy(message:types.Message):
    user_id = message.from_user.id
    user_data[user_id]['state'] = 'show_vacancies'
    city = message.text
    if city in user_data[user_id]['lang_dict']['cities']:
        user_data[user_id]['temp'] = city
    elif city == 'Назад':
        city = user_data[user_id]['temp']
    branches = user_data[user_id]['lang_dict']['cities'][city]
    print(6, user_data)
    print(branches)
    buttons = []
    for branch in branches:
        buttons.append([types.KeyboardButton(text=branch)])
    buttons.append([types.KeyboardButton(text='Назад')])
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer('Выберите филиал', reply_markup=keyboard)


async def choose_branch(message:types.Message):
    user_id = message.from_user.id
    user_data[user_id]['state'] = 'choose_branch'
    branch = message.text
    # city = user_data[user_id]['temp']
    city = 'Ташкент'
    vacancies = user_data[user_id]['lang_dict']['cities'][city][branch]['vacancy']
    buttons = []
    for vac in vacancies:
        buttons.append([types.KeyboardButton(text=vac)])
    buttons.append([types.KeyboardButton(text='Назад')])
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    print(7, user_data)
    await message.answer('Выберите вакансию:', reply_markup=keyboard)




async def main():
    await dp.start_polling(bot)

asyncio.run(main())
