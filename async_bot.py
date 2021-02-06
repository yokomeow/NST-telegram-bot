import config
import logging
import nst
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.executor import start_webhook

from shutil import copyfile


# webhook settings
# WEBHOOK_HOST = 'https://your.domain'
# WEBHOOK_PATH = '/path/to/api'
# WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
# WEBAPP_HOST = 'localhost'  # or ip
# WEBAPP_PORT = 3001

# port
# PORT = int(os.environ.get('PORT', 5000))

# logging level
logging.basicConfig(level=logging.INFO)

# initialize bot
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


# start message
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    sti = open('images/source/start-sticker.webp', 'rb')
    await bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup_general = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1_general = types.KeyboardButton('Прикрепить фото 🌅')
    button2_general = types.KeyboardButton('Покажи пример 🤷‍♀️')

    markup_general.add(button1_general, button2_general)

    await bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, стильный '
                                            'бот, который превратит любую твою фотографию в произведение '
                                            'искусства!'.format(message.from_user, await bot.get_me()),
                           parse_mode='html', reply_markup=markup_general)
    await bot.send_message(message.chat.id, 'Остались вопросы? ➡️ /help')


# help
@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Я бот, который может перенести стиль с одной фотографии на другую. Тебе '
                                            'лишь нужно отправить мне фото, которое ты хочешь преобразить. Далее, '
                                            'тебе будет предложено несколько стилей на выбор. Чтобы посмотреть пример '
                                            'обработки, можешь ткнуть на кнопку "Покажи пример 🤷‍♀️"')


# chat
@dp.message_handler(content_types=['text'])
async def chat(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Прикрепить фото 🌅':
            await bot.send_message(message.chat.id,
                                   'Пожалуйста, отправьте мне фото, которое хотите обработать. '
                                   'Рекомендуется, чтобы объект на фото располагался по центру, так как в процессе '
                                   'обработки фото кадрируется.')
        elif message.text == 'Покажи пример 🤷‍♀️':
            content_pic = open('images/source/city-sunset.jpg', 'rb')
            result_pic = open('images/results/result-4.png', 'rb')

            reply_markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
            reply_button1 = types.InlineKeyboardButton('Круто! 😍', callback_data='good')
            reply_button2 = types.InlineKeyboardButton('Так себе.. 😒', callback_data='bad')

            reply_markup.add(reply_button1, reply_button2)

            await bot.send_photo(message.chat.id, content_pic)
            await bot.send_message(message.chat.id, 'Например, ты отправляешь фото города на закате... ⬆️')
            await bot.send_photo(message.chat.id, result_pic)
            await bot.send_message(message.chat.id, '...а я делаю из него фото дневного города! ⬆️',
                                   reply_markup=reply_markup)

        else:
            await bot.send_message(message.chat.id, 'Я не знаю, что ответить 😿')


# save photo
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    await message.photo[-1].download('./images/source/content_image.jpg')
    await bot.send_message(message.chat.id, 'Фото успешно загружено!')

    style_reply_markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    style_reply_button1 = types.InlineKeyboardButton('Ван Гог (1)', callback_data='gogh')
    style_reply_button2 = types.InlineKeyboardButton('Пикассо (2)', callback_data='picasso')
    style_reply_button3 = types.InlineKeyboardButton('Афремов (3)', callback_data='afremov')

    style_reply_markup.add(style_reply_button1, style_reply_button2, style_reply_button3)

    style_pic1 = open('images/source/van_gogh.jpg', 'rb')
    style_pic2 = open('images/source/picasso.jpg', 'rb')
    style_pic3 = open('images/source/afremov.jpg', 'rb')

    await bot.send_photo(message.chat.id, style_pic1)
    await bot.send_photo(message.chat.id, style_pic2)
    await bot.send_photo(message.chat.id, style_pic3)
    await bot.send_message(message.chat.id, 'Теперь осталось выбрать стиль:', reply_markup=style_reply_markup)


# callback
@dp.callback_query_handler(lambda call: True)
async def callback_inline(call):
    try:
        if call.message:
            # example feedback
            if call.data == 'good':
                await bot.send_message(call.message.chat.id, 'Рад, что тебе понравилось! 🥰')
            elif call.data == 'bad':
                await bot.send_message(call.message.chat.id, 'Люди никогда не понимали современников... 😔')
            # style
            elif call.data == 'gogh':
                await bot.send_message(call.message.chat.id, '"Звездная Ночь" - хороший выбор! 🌃')
                copyfile('images/source/van_gogh.jpg', 'images/source/style_image.jpg')
                await launch_nst(call.message)
            elif call.data == 'picasso':
                await bot.send_message(call.message.chat.id, 'Пикассо - замечательно! 🌚')
                copyfile('images/source/picasso.jpg', 'images/source/style_image.jpg')
                await launch_nst(call.message)
            elif call.data == 'afremov':
                await bot.send_message(call.message.chat.id, 'Чудесная задумка! 🌺')
                copyfile('images/source/afremov.jpg', 'images/source/style_image.jpg')
                await launch_nst(call.message)
            # result feedback
            elif call.data == 'amazing':
                await bot.send_message(call.message.chat.id, 'Круто! Сам в шоке, что так классно получилось! 💥')
            elif call.data == 'nice':
                await bot.send_message(call.message.chat.id, 'Супер! 👍')
            elif call.data == 'ok':
                await bot.send_message(call.message.chat.id, 'Может, в следующий раз у меня лучше получится. 😕')
            elif call.data == 'gross':
                await bot.send_message(call.message.chat.id, 'Надеюсь, это останется между нами... 👉👈')

            # remove inline buttons
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='...',
                                        reply_markup=None)
    except Exception as e:
        print(repr(e))

1589660470:AAF6u8t2kdtwO3smV_pODxUqndIOo0OmZww
# launch style transfer
async def launch_nst(message):
    # print('ok')
    content_image_name = 'images/source/content_image.jpg'
    style_image_name = 'images/source/style_image.jpg'
    content = open(content_image_name, 'rb')
    style = open(style_image_name, 'rb')

    await bot.send_photo(message.chat.id, content)
    await bot.send_message(message.chat.id, 'Начал обработку данной фотографии. ⚙️')

    await bot.send_photo(message.chat.id, style)
    await bot.send_message(message.chat.id, 'С таким стилем.')

    await bot.send_message(message.chat.id, 'Пожалуйста, подождите. Это займет примерно 6-7 минут...')

    await nst.main(content_image_name, style_image_name)

    await bot.send_message(message.chat.id, 'Готово!')
    result = open('images/results/bot-result.png', 'rb')
    await bot.send_photo(message.chat.id, result)

    result_reply_markup = types.InlineKeyboardMarkup(row_width=2)
    result_reply_button1 = types.InlineKeyboardButton('Вау, шикарно!', callback_data='amazing')
    result_reply_button2 = types.InlineKeyboardButton('Очень даже неплохо', callback_data='nice')
    result_reply_button3 = types.InlineKeyboardButton('Нормально', callback_data='ok')
    result_reply_button4 = types.InlineKeyboardButton('Ой...кошмар', callback_data='gross')

    result_reply_markup.add(result_reply_button1, result_reply_button2, result_reply_button3, result_reply_button4)

    await bot.send_message(message.chat.id, 'Ну, как тебе? 🧐', reply_markup=result_reply_markup)
    await bot.send_message(message.chat.id, 'Чтобы попробовать еще раз, просто отправь мне новое фото. ☺️')


# async def on_startup(dp):
#    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


# async def on_shutdown(dp):
#    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
#    await bot.delete_webhook()

    # Close DB connection (if used)
#    await dp.storage.close()
#    await dp.storage.wait_closed()

 #   logging.warning('Bye!')


# launch long polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    #start_webhook(listen='0.0.0.0', port=int(PORT), url_path=config.TOKEN)
    #executor.set_webhook('https://style-tg-bot.herokuapp.com/' + config.TOKEN)
    #start_webhook(
    #    dispatcher=dp,
    #    webhook_path=WEBHOOK_PATH,
    #    on_startup=on_startup,
    #    on_shutdown=on_shutdown,
    #    skip_updates=True,
    #    host=WEBAPP_HOST,
    #    port=WEBAPP_PORT,
    #)
