import telebot
import config
import nst
from shutil import copyfile

from telebot import types


#bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
	sti = open('images/source/start-sticker.webp', 'rb')
	bot.send_sticker(message.chat.id, sti)
	
	# keyboard
	markup_general = types.ReplyKeyboardMarkup(resize_keyboard=True)
	button1_general = types.KeyboardButton('Прикрепить фото 🌅')
	button2_general = types.KeyboardButton('Покажи пример 🤷‍♀️')
	
	markup_general.add(button1_general, button2_general)
	
	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, \
					 стильный бот, который превратит любую твою фотографию в произведение искусства!".format(message.from_user, bot.get_me()), \
					 parse_mode='html', reply_markup=markup_general)
	

@bot.message_handler(content_types=['text'])
def chat(message):
	if message.chat.type == 'private':
		if message.text == 'Прикрепить фото 🌅':
			bot.send_message(message.chat.id,
							 'Пожалуйста, отправьте мне фото в виде файла, которое хотите обработать. Рекомендуется, чтобы объект на фото располагался по центру, так как в процессе обработки фото кадрируется.')

		elif message.text == 'Покажи пример 🤷‍♀️':
			content_pic = open('images/source/city-sunset.jpg', 'rb')
			result_pic = open('images/results/result-4.png', 'rb')
			
			reply_markup = types.InlineKeyboardMarkup(row_width=2)
			reply_button1 = types.InlineKeyboardButton('Круто! 😍', callback_data='good')
			reply_button2 = types.InlineKeyboardButton('Так себе.. 😒', callback_data='bad')
			
			reply_markup.add(reply_button1, reply_button2)
			
			bot.send_photo(message.chat.id, content_pic)
			bot.send_message(message.chat.id, 'Например, ты отправляешь фото города на закате... ⬆️')
			bot.send_photo(message.chat.id, result_pic)
			bot.send_message(message.chat.id, '...а я делаю из него фото дневного города! ⬆️', reply_markup=reply_markup)
			
		else:
			bot.send_message(message.chat.id, 'Я не знаю, что ответить 😿')

@bot.message_handler(content_types=['document', 'Document'])  # 'photo', 'Photo'
def photo_processing(message):
	if message.chat.type == 'private':
		file_name = message.document.file_name
		file_id = message.document.file_id
		file_id_info = bot.get_file(message.document.file_id)
		downloaded_file = bot.download_file(file_id_info.file_path)
		with open('./images/source/' + 'content_image.jpg', 'wb') as content_image:
			content_image.write(downloaded_file)
		#print(message.photo[0])
		#bot.download_file(message.photo[0].file_id)
		bot.send_message(message.chat.id, 'Фото успешно загружено!')

		style_reply_markup = types.InlineKeyboardMarkup(row_width=2)
		style_reply_button1 = types.InlineKeyboardButton('Ван Гог', callback_data='gogh')
		style_reply_button2 = types.InlineKeyboardButton('Пикассо', callback_data='picasso')
		style_reply_button3 = types.InlineKeyboardButton('Моне', callback_data='monet')

		style_reply_markup.add(style_reply_button1, style_reply_button2, style_reply_button3)

		style_pic1 = open('images/source/van_gogh.jpg', 'rb')
		style_pic2 = open('images/source/picasso.jpg', 'rb')
		style_pic3 = open('images/source/monet.jpg', 'rb')

		bot.send_photo(message.chat.id, style_pic1)
		bot.send_photo(message.chat.id, style_pic2)
		bot.send_photo(message.chat.id, style_pic3)
		bot.send_message(message.chat.id, 'Теперь осталось выбрать стиль:', reply_markup=style_reply_markup)
			

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			# example feedback
			if call.data == 'good':
				bot.send_message(call.message.chat.id, 'Рад, что тебе понравилось! 🥰')
			elif call.data == 'bad':
				bot.send_message(call.message.chat.id, 'Люди никогда не понимали современников... 😔')
			# style
			elif call.data == 'gogh':
				bot.send_message(call.message.chat.id, '"Звездная Ночь" - хороший выбор! 🌃')
				copyfile('images/source/van_gogh.jpg', 'images/source/style_image.jpg')
				launch_nst(call.message)
			elif call.data == 'picasso':
				bot.send_message(call.message.chat.id, 'Пикассо - замечательно! 🌚')
				copyfile('images/source/picasso.jpg', 'images/source/style_image.jpg')
				launch_nst(call.message)
			elif call.data == 'monet':
				bot.send_message(call.message.chat.id, 'Моне - чудесная задумка! 🌺')
				copyfile('images/source/monet.jpg', 'images/source/style_image.jpg')
				launch_nst(call.message)
			# result feedback
			elif call.data == 'amazing':
				bot.send_message(call.message.chat.id, 'Круто! Сам в шоке, что так классно получилось! 💥')
			elif call.data == 'nice':
				bot.send_message(call.message.chat.id, 'Супер! 👍')
			elif call.data == 'ok':
				bot.send_message(call.message.chat.id, 'Может, в следующий раз у меня лучше получится. 😕')
			elif call.data == 'gross':
				bot.send_message(call.message.chat.id, 'Надеюсь, это останется между нами... 👉👈')

			# remove inline buttons
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= '...',
								  reply_markup=None)
	except Exception as e:
		print(repr(e))
				

def launch_nst(message):
	print('ok')
	content_image_name = 'images/source/content_image.jpg'
	style_image_name = 'images/source/style_image.jpg'
	content = open(content_image_name, 'rb')
	style = open(style_image_name, 'rb')

	bot.send_photo(message.chat.id, content)
	bot.send_message(message.chat.id, 'Начал обработку данной фотографии. ⚙️')

	bot.send_photo(message.chat.id, style)
	bot.send_message(message.chat.id, 'С таким стилем.')

	bot.send_message(message.chat.id, 'Пожалуйста, подождите. Это займет примерно 6 минут...')

	nst.main(content_image_name, style_image_name)

	bot.send_message(message.chat.id, 'Готово!')
	result = open('images/results/bot-result.png', 'rb')
	bot.send_photo(message.chat.id, result)

	result_reply_markup = types.InlineKeyboardMarkup(row_width=2)
	result_reply_button1 = types.InlineKeyboardButton('Вау, шикарно!', callback_data='amazing')
	result_reply_button2 = types.InlineKeyboardButton('Очень даже неплохо', callback_data='nice')
	result_reply_button3 = types.InlineKeyboardButton('Нормально', callback_data='ok')
	result_reply_button4 = types.InlineKeyboardButton('Ой...кошмар', callback_data='gross')

	result_reply_markup.add(result_reply_button1, result_reply_button2, result_reply_button3, result_reply_button4)

	bot.send_message(message.chat.id, 'Ну, как тебе? 🧐', reply_markup=result_reply_markup)


# RUN
bot.polling(none_stop=True)
