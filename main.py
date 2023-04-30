import logging
from telegram.ext import (Application,
                          CommandHandler,
                          InlineQueryHandler,
                          CallbackContext,
                          CallbackQueryHandler,
                          ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN
import CoinGlass
from exchanges import all_ex_price
from CatPic import get_images

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user

    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Этот бот подскажет тебе, какой сейчас курс у нужной тебе монеты" + "\n"
        + rf"Соотношение лонговых и шортовых позиций" + '\n' + '\n' + 'Для управления используйте команды из /help',
    )
    return 'first'


async def help(update, context):
    """Отправляюет пользователю описание команд"""
    await update.message.reply_text('Бот имеет следующие команды:\n/price - выводит список цен на 7 различных биржах\n'
                                    '/ratio - выводит соотноешние лонгистов и шортистов на BTC\n'
                                    '/cat - интересная функция, позволяющая насладиться преимуществами технологий')


async def ratio(upadte, context):
    """Собирает данные с сайта CoinGlass.com и отправляет их пользователю"""
    if 'timeframe' not in context.chat_data:
        timeframe = 'h1'
    else:
        timeframe = context.chat_data['timeframe']
    cg_data = CoinGlass.get_data(timeframe=timeframe)
    if cg_data.__class__ != Exception.__class__:
        longs, shorts = cg_data
        await upadte.message.reply_text(f"Позиций лонг: {longs}; позиций шорт: {shorts}")
    else:
        await upadte.message.reply_text(f"Небольшие неподалки, попорбуйте позднее")


async def price(update, context):
    """Собирает данные о цене с топ 7 бирж и отправляет их пользователю в отсортированном порядке."""

    total = all_ex_price()
    mes = 'Цены на биржах:\n'
    all_prices = sorted([(key, value) for key, value in total.items()], key=lambda x: x[1])
    for ex in range(len(all_prices)):
        mes = mes + str((ex + 1)) + ") " + all_prices[ex][0].capitalize() + ": " + str(all_prices[ex][1]) + "\n\n"
    mes = mes.rstrip()
    await update.message.reply_text(mes)


async def cat(update, context):
    """Загружает из интернета рандомную картинку с котом"""
    link = get_images()
    await update.message.reply_text(link)


def main():
    application = Application.builder().token(token=BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('cat', cat))
    application.add_handler(CommandHandler('ratio', ratio))
    application.add_handler(CommandHandler('price', price))

    application.run_polling()


if __name__ == "__main__":
    main()
