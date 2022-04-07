from click import command
import config
import telebot
import random
import os

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['start'])

def welcome(message):
	sti = open('stickers/1.webp', 'rb')

	# Keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	item1 = types.KeyboardButton("хочу смешнявку")
	item2 = types.KeyboardButton("Привет")
	markup.add(item1, item2)

	bot.send_sticker(message.chat.id, sti)
	bot.send_message (message.chat.id, "Привет, {0.first_name}!\nЯ бот комплиментов <b>{1.first_name}</b>!\nЛапочка 😘😘😘😘😘😘\n❤❤❤❤❤❤".format(message.from_user, bot.get_me()),
	parse_mode='html', reply_markup = markup)

@bot.message_handler(content_types = ['text'])
def message_lov(message):
	if message.chat.type == 'private':
		if message.text == 'хочу смешнявку':
			arts = open(config.DIR + random.choice(os.listdir(config.DIR)), 'rb')
			bot.send_sticker(message.chat.id, arts)
		elif message.text == 'Привет':
			markup = types.InlineKeyboardMarkup()
			item1 = types.InlineKeyboardButton("Хочу комплимент", callback_data='compliment')
			item2 = types.InlineKeyboardButton("Ты фуфлыжник", callback_data='badword')
			item3 = types.InlineKeyboardButton("Хочу чаю", callback_data='teatime')

			markup.add(item1, item2, item3)

			bot.send_message(message.chat.id, "И так...\n", reply_markup = markup)
		else :
			bot.send_message(message.chat.id, "Я не знаю что ответить!")


@bot.callback_query_handler(func = lambda call : True)
def ft_answ(call):
	try :
		if call.message:
			if call.data == 'compliment':
				
				# compliments
				n_compliments = random.randint(1,3)
				if n_compliments == 1:
					compliments = "Ты великолепный человек!"
				elif n_compliments == 2:
					compliments = "У тебя самая красивая улыбка!"
				elif n_compliments == 3 :
					compliments = "Ты, как закат...\nМожно смотреть на тебя вечность!"
				bot.send_message(call.message.chat.id, compliments)

			elif call.data == 'badword':
				bot.send_message(call.message.chat.id, "😢😢😢\n😢😢😢\n😢😢😢\n😢😢😢\n😢😢😢")

			elif call.data == 'teatime':
				tea = open('tea_time/1.webp', 'rb')
				bot.send_sticker(call.message.chat.id, tea)
				tea = open('tea_time/2.webp', 'rb')
				bot.send_sticker(call.message.chat.id, tea)
			else :
				bot.send_message(call.message.chat.id, "Я не знаю что ответить!")

			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Привет",
			reply_markup=None)

			bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Error")

	except Exception as e:
		print(repr(e))

bot.polling(non_stop=True)
