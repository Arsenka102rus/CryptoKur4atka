import logging

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

from exchanges import all_ex_price
from CatPic import get_images
import CoinGlass
from config import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
total_keyboard = types.InlineKeyboardMarkup(row_width=2)
total_keyboard.add(types.InlineKeyboardButton(text='Price', callback_data='price'))
total_keyboard.add(types.InlineKeyboardButton(text='Longs&Shorts', callback_data='ratio'))
total_keyboard.add(types.InlineKeyboardButton(text='Сat', callback_data='cat'))

timeframes_keyboard = types.InlineKeyboardMarkup(row_width=2)
cb = CallbackData('timeframe', 'time', 'figure')
timeframes_keyboard.add(types.InlineKeyboardButton(text='5m', callback_data=cb.new(time='m', figure='5')))
timeframes_keyboard.add(types.InlineKeyboardButton(text='30m', callback_data=cb.new(time='m', figure='30')))
timeframes_keyboard.add(types.InlineKeyboardButton(text='1h', callback_data=cb.new(time='h', figure='1')))
timeframes_keyboard.add(types.InlineKeyboardButton(text='4h', callback_data=cb.new(time='h', figure='4')))
timeframes_keyboard.add(types.InlineKeyboardButton(text='24h', callback_data=cb.new(time='h', figure='24')))
timeframes_keyboard.add(types.InlineKeyboardButton(text='< Назад', callback_data='back'))

user_data = {}


class ChooseTimeframe(StatesGroup):
    choosing_timeframe = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message | types.CallbackQuery):
    """
    This handler will be called when user sends `/start` or `/help` command
    Creates standard timeframe and coin for current user
    """
    user_id = message.from_user.id
    if user_id not in user_data:
        data = {'timeframe': 'h1',
                'coin': 'BTC'}
        user_data[user_id] = data
    if isinstance(message, types.Message):
        await message.answer("Привет, этот бот подскажет тебе курсы по интересующей тебя монете\n"
                             "И соотношение лонгистов и шортистов\n"
                             "Для управления используй команды из блока /help", reply_markup=total_keyboard)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text("Привет, этот бот подскажет тебе курсы по интересующей тебя монете\n"
                                        "И соотношение лонгистов и шортистов\n"
                                        "Для управления используй команды из блока /help", reply_markup=total_keyboard)


@dp.message_handler(commands=['help'])
async def help(message):
    """Отправляюет пользователю описание команд"""
    await message.answer('Бот имеет следующие команды:\n/price - выводит список цен на 7 различных биржах\n'
                         '/ratio - выводит соотношение лонгистов и шортистов на BTC\n'
                         '/cat - интересная функция, позволяющая насладиться преимуществами технологий')


async def ratio(message: types.Message | types.CallbackQuery):
    """Собирает данные с сайта CoinGlass.com и отправляет их пользователю"""
    user_id = message.from_user.id
    data = user_data[user_id]
    timeframe = data['timeframe']
    ratio_keyboard = types.InlineKeyboardMarkup(row_width=2)
    ratio_keyboard.add(types.InlineKeyboardButton(text='Price', callback_data='price'))
    ratio_keyboard.add(types.InlineKeyboardButton(text='Longs&Shorts', callback_data='ratio'))
    ratio_keyboard.add(types.InlineKeyboardButton(text='Сat', callback_data='cat'))
    ratio_keyboard.add(types.InlineKeyboardButton(text='Поменять таймфрейм', callback_data='change_timeframe'))
    cg_data = CoinGlass.get_data(timeframe=timeframe)
    if cg_data.__class__ != Exception.__class__ and cg_data != 'data':
        longs, shorts = cg_data
        mes = f"Позиций лонг: {longs}; позиций шорт: {shorts}\nТаймрфейм: {timeframe}"
    else:
        mes = f"Небольшие неполадки, попробуйте позднее"
    if isinstance(message, types.Message):
        await message.answer(mes)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(mes, reply_markup=ratio_keyboard)


@dp.callback_query_handler(text='change_timeframe')
async def change_timeframe(message: Message):
    user_id = message.from_user.id
    data = user_data[user_id]
    timeframe = data['timeframe']
    if isinstance(message, Message):
        await message.answer(text=f'Текущий таймфрейм: {timeframe}\n' +
                                  f'Нажмите на кнопку ниже, чтобы изменить', reply_markup=timeframes_keyboard)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text=f'Текущий таймфрейм: {timeframe}\n' +
                                             f'Нажмите на кнопку ниже, чтобы изменить',
                                        reply_markup=timeframes_keyboard)


@dp.callback_query_handler(cb.filter())
async def timeframe_chosen(call: types.CallbackQuery, callback_data: dict):
    timeframe = callback_data['time'] + callback_data['figure']
    user_id = call.from_user.id
    data = user_data[user_id]
    del data['timeframe']
    data['timeframe'] = timeframe
    await change_timeframe(call)


@dp.callback_query_handler(text='ratio')
async def inline_ratio(call):
    await ratio(call)


@dp.message_handler(commands=['ratio'])
async def message_ratio(message):
    await ratio(message)


async def price(message: types.CallbackQuery | types.Message):
    """Собирает данные о цене с топ 7 бирж и отправляет их пользователю в отсортированном порядке."""
    user_id = message.from_user.id
    data = user_data[user_id]
    coin = data['coin']
    total = all_ex_price(coin=coin)
    mes = f'Цены на биржах:\n'
    all_prices = sorted([(key, value) for key, value in total.items()], key=lambda x: x[1])
    for ex in range(len(all_prices)):
        mes = mes + str((ex + 1)) + ") " + all_prices[ex][0].capitalize() + ": " + str(all_prices[ex][1]) + "\n\n"
    mes = mes.rstrip()
    if isinstance(message, types.Message):
        await message.answer(mes)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(mes, reply_markup=total_keyboard)


@dp.callback_query_handler(text='price')
async def inline_price(call: types.CallbackQuery):
    await price(call)


@dp.message_handler(commands=['price'])
async def message_price(message: types.Message):
    await price(message)


async def cat(message):
    """Загружает из интернета рандомную картинку с котом"""
    link = get_images()
    if isinstance(message, types.Message):
        await message.reply(link)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(link, reply_markup=total_keyboard)


@dp.callback_query_handler(text='cat')
async def inline_cat(call):
    await cat(call)


@dp.message_handler(commands=['cat'])
async def message_cat(message):
    await cat(message)


@dp.callback_query_handler(text='back')
async def message_cat(call):
    await start(call)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
