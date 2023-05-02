import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

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


@dp.message_handler(commands=['start'])
async def start(message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    await message.reply("Привет, этот бот подскажет тебе курсы по интересующей тебя монете\n"
                        "И соотношение лонгистов и шортистов\n"
                        "Для управления используй команды из блока /help", reply_markup=total_keyboard)


@dp.message_handler(commands=['help'])
async def help(message):
    """Отправляюет пользователю описание команд"""
    await message.reply('Бот имеет следующие команды:\n/price - выводит список цен на 7 различных биржах\n'
                        '/ratio - выводит соотношение лонгистов и шортистов на BTC\n'
                        '/cat - интересная функция, позволяющая насладиться преимуществами технологий')


async def ratio(message):
    """Собирает данные с сайта CoinGlass.com и отправляет их пользователю"""
    timeframe = 'h1'
    cg_data = CoinGlass.get_data(timeframe=timeframe)
    if cg_data.__class__ != Exception.__class__:
        longs, shorts = cg_data
        mes = f"Позиций лонг: {longs}; позиций шорт: {shorts}"
    else:
        mes = f"Небольшие неполадки, попробуйте позднее"
    if isinstance(message, types.Message):
        await message.reply(mes)
    elif isinstance(message, types.CallbackQuery):
        await message.message.reply(mes, reply_markup=total_keyboard)


@dp.callback_query_handler(text='ratio')
async def inline_ratio(call):
    await ratio(call)


@dp.message_handler(commands=['ratio'])
async def message_ratio(message):
    await ratio(message)


async def price(message: types.CallbackQuery | types.Message):
    """Собирает данные о цене с топ 7 бирж и отправляет их пользователю в отсортированном порядке."""
    total = all_ex_price()
    mes = f'Цены на биржах:\n'
    all_prices = sorted([(key, value) for key, value in total.items()], key=lambda x: x[1])
    for ex in range(len(all_prices)):
        mes = mes + str((ex + 1)) + ") " + all_prices[ex][0].capitalize() + ": " + str(all_prices[ex][1]) + "\n\n"
    mes = mes.rstrip()
    if isinstance(message, types.Message):
        await message.reply(mes)
    elif isinstance(message, types.CallbackQuery):
        await message.message.reply(mes, reply_markup=total_keyboard)


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
        await message.message.reply(link, reply_markup=total_keyboard)


@dp.callback_query_handler(text='cat')
async def inline_cat(call):
    await cat(call)


@dp.message_handler(commands=['cat'])
async def message_cat(message):
    await cat(message)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
