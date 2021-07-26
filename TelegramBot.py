import telebot
from telebot import types
import mysql.connector

bot = telebot.TeleBot('******')
mHost="******"
mUser="******"
mPswrd="******"
mDb="******"
adminChatID = 12****** #person who receives notifications when new questions are asked. Must have active chat with bot

question = None

@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton('🏫 Приймальна комісія')
	btn2 = types.KeyboardButton('🗄 Спеціальності')
	btn3 = types.KeyboardButton('📕 Правила вступної кампанії')
	btn4 = types.KeyboardButton('🗓 Етапи вступної кампанії')
	btn5 = types.KeyboardButton('🚪 День відкритих дверей')
	btn6 = types.KeyboardButton('📝 Підготовчі курси')
	btn7 = types.KeyboardButton('❓ Часті запитання')
	markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
	send_mess = f"Вітаю, {message.from_user.first_name} {message.from_user.last_name}!\nЦе інформаційний бот для вступників, які вступатимуть до СПФК ЦНТУ, та їх батьків."
	bot.send_message(message.chat.id, send_mess, parse_mode='Markdown', reply_markup=markup)

def process_question_step(message):
	global question
	question = message.text
	
	if len(question) > 15:
		final_message = "Залиште ваші контакти (email або телефон):"
		bot.send_message(message.chat.id, final_message)
		bot.register_next_step_handler(message, process_contact_step)
	else:
		bot.send_message(message.chat.id, "Питання дуже коротке!")
	
def process_contact_step(message):
	contact = message.text

	mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
	mycursor = mydb.cursor()
	mycursor.execute('SELECT text FROM question')
	myresult = mycursor.fetchone()
	previous = ''.join(myresult)
	mycursor.close()
	mydb.close()

	new='Питання: ' + question + '\nКонтакти: ' + contact + '\n\n'
	previous+= new

	mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
	mycursor = mydb.cursor()
	sql = "UPDATE question SET text = '"+previous+"' WHERE id=1"
	mycursor.execute(sql)
	mydb.commit()
	mycursor.close()
	mydb.close()

	final_message = "Ваше питання прийнято ✅\nМи зв'жемось з вами найближчим часом."
	bot.send_message(adminChatID, "Нове питання: \n" + question + "\nКонтакти: " + contact)
	bot.send_message(message.chat.id, final_message, parse_mode='Markdown')
	

@bot.message_handler(content_types=['text'])

def mess(message):
	get_message_bot = message.text

	if get_message_bot == '🏫 Приймальна комісія':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('🕣 Графік роботи')
		btn2 = types.KeyboardButton('☎️ Контакти')
		btn3 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3)
		final_message = "Оберіть дію з меню:"

	elif get_message_bot == '🗄 Спеціальності':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('🏫 Приймальна комісія')
		btn2 = types.KeyboardButton('🗄 Спеціальності')
		btn3 = types.KeyboardButton('📕 Правила вступної кампанії')
		btn4 = types.KeyboardButton('🗓 Етапи вступної кампанії')
		btn5 = types.KeyboardButton('🚪 День відкритих дверей')
		btn6 = types.KeyboardButton('📝 Підготовчі курси')
		btn7 = types.KeyboardButton('❓ Часті запитання')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM specialty')
		myresult = mycursor.fetchone()
		final_message = ''.join(myresult)
		mycursor.close()
		mydb.close()

	elif get_message_bot == '📕 Правила вступної кампанії':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('📖 Правила прийому')
		btn2 = types.KeyboardButton('🗞 Перелік конкурсних предметів')
		btn3 = types.KeyboardButton('🗃 Перелік документів')
		btn4 = types.KeyboardButton('🧾 Державне замовлення')
		btn5 = types.KeyboardButton('💶 Вартість навчання')
		btn6 = types.KeyboardButton('📚 Програма підготовки')
		btn7 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
		final_message = "Оберіть дію з меню:"
	
	elif get_message_bot == '🗓 Етапи вступної кампанії':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('⏳ Терміни подачі документів')
		btn2 = types.KeyboardButton('📆 Розклад вступних випробувань')
		btn3 = types.KeyboardButton('🗳 Результати вступних випробувань')
		btn4 = types.KeyboardButton('📉 Рейтинговий список')
		btn5 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5)
		final_message = "Оберіть дію з меню:"

	elif get_message_bot == '🚪 День відкритих дверей':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('🏫 Приймальна комісія')
		btn2 = types.KeyboardButton('🗄 Спеціальності')
		btn3 = types.KeyboardButton('📕 Правила вступної кампанії')
		btn4 = types.KeyboardButton('🗓 Етапи вступної кампанії')
		btn5 = types.KeyboardButton('🚪 День відкритих дверей')
		btn6 = types.KeyboardButton('📝 Підготовчі курси')
		btn7=types.KeyboardButton('❓ Часті запитання')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="День відкритих дверей"')
		myresult = mycursor.fetchone()
		final_message = ''.join(myresult)
		mycursor.close()
		mydb.close()

	elif get_message_bot == '📝 Підготовчі курси':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('🏫 Приймальна комісія')
		btn2 = types.KeyboardButton('🗄 Спеціальності')
		btn3 = types.KeyboardButton('📕 Правила вступної кампанії')
		btn4 = types.KeyboardButton('🗓 Етапи вступної кампанії')
		btn5 = types.KeyboardButton('🚪 День відкритих дверей')
		btn6 = types.KeyboardButton('📝 Підготовчі курси')
		btn7=types.KeyboardButton('❓ Часті запитання')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
		final_message = "*Підготовчі курси:*\n\n"

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="Підготовчі курси"')
		myresult = mycursor.fetchone()
		final_message += ''.join(myresult)
		mycursor.close()
		mydb.close()
	
	elif get_message_bot == '🗨 Додатково':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('🔔 Підписатися')
		btn2 = types.KeyboardButton('🔕 Відписатися')
		btn3 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3)
		final_message = "Оберіть дію з меню:"

	elif get_message_bot == '🔙 Меню':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('🏫 Приймальна комісія')
		btn2 = types.KeyboardButton('🗄 Спеціальності')
		btn3 = types.KeyboardButton('📕 Правила вступної кампанії')
		btn4 = types.KeyboardButton('🗓 Етапи вступної кампанії')
		btn5 = types.KeyboardButton('🚪 День відкритих дверей')
		btn6 = types.KeyboardButton('📝 Підготовчі курси')
		btn7 = types.KeyboardButton('❓ Часті запитання')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
		final_message = "Головне меню"

	elif get_message_bot == '🕣 Графік роботи':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('🕣 Графік роботи')
		btn2 = types.KeyboardButton('☎️ Контакти')
		btn3 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3)
		final_message='*Графік роботи приймальної комісії:* \n\n'

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM openinghours')
		myresult = mycursor.fetchone()
		final_message += ''.join(myresult)
		mycursor.close()
		mydb.close()

	elif get_message_bot == '☎️ Контакти':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('🕣 Графік роботи')
		btn2 = types.KeyboardButton('☎️ Контакти')
		btn3 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3)
		final_message = "*Контакти:* \n\n"

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM contacts')
		myresult = mycursor.fetchone()
		final_message += ''.join(myresult)
		mycursor.close()
		mydb.close()

	elif get_message_bot == '❓ Часті запитання':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('📮 Запитати')
		btn2 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2)
		final_message = "*Відповіді на часті запитання:* \n\n"

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM faq ORDER BY id')
		myresult = mycursor.fetchone()
		final_message += ''.join(myresult)
		mycursor.close()
		mydb.close()

		final_message += "\n\n_Не знайшли відповідь? Залиште запитання та контактні дані і ми зв'яжемось з вами_ \n\n"

	elif get_message_bot == '📖 Правила прийому':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('📖 Правила прийому')
		btn2 = types.KeyboardButton('🗞 Перелік конкурсних предметів')
		btn3 = types.KeyboardButton('🗃 Перелік документів')
		btn4 = types.KeyboardButton('🧾 Державне замовлення')
		btn5 = types.KeyboardButton('💶 Вартість навчання')
		btn6 = types.KeyboardButton('📚 Програма підготовки')
		btn7 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="Правила прийому"')
		myresult = mycursor.fetchone()
		final_message = ''.join(myresult)
		mycursor.close()
		mydb.close()
	
	elif get_message_bot == '🧾 Державне замовлення':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('📖 Правила прийому')
		btn2 = types.KeyboardButton('🗞 Перелік конкурсних предметів')
		btn3 = types.KeyboardButton('🗃 Перелік документів')
		btn4 = types.KeyboardButton('🧾 Державне замовлення')
		btn5 = types.KeyboardButton('💶 Вартість навчання')
		btn6 = types.KeyboardButton('📚 Програма підготовки')
		btn7 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="Державне замовлення"')
		myresult = mycursor.fetchone()
		final_message = ''.join(myresult)
		mycursor.close()
		mydb.close()

	elif get_message_bot == '💶 Вартість навчання':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('📖 Правила прийому')
		btn2 = types.KeyboardButton('🗞 Перелік конкурсних предметів')
		btn3 = types.KeyboardButton('🗃 Перелік документів')
		btn4 = types.KeyboardButton('🧾 Державне замовлення')
		btn5 = types.KeyboardButton('💶 Вартість навчання')
		btn6 = types.KeyboardButton('📚 Програма підготовки')
		btn7 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="Вартість навчання"')
		myresult = mycursor.fetchone()
		final_message = ''.join(myresult)
		mycursor.close()
		mydb.close()

	elif get_message_bot == '📚 Програма підготовки':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('📖 Правила прийому')
		btn2 = types.KeyboardButton('🗞 Перелік конкурсних предметів')
		btn3 = types.KeyboardButton('🗃 Перелік документів')
		btn4 = types.KeyboardButton('🧾 Державне замовлення')
		btn5 = types.KeyboardButton('💶 Вартість навчання')
		btn6 = types.KeyboardButton('📚 Програма підготовки')
		btn7 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="Програма підготовки"')
		myresult = mycursor.fetchone()
		final_message = ''.join(myresult)
		mycursor.close()
		mydb.close()
	
	elif get_message_bot == '🗞 Перелік конкурсних предметів':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('📖 Правила прийому')
		btn2 = types.KeyboardButton('🗞 Перелік конкурсних предметів')
		btn3 = types.KeyboardButton('🗃 Перелік документів')
		btn4 = types.KeyboardButton('🧾 Державне замовлення')
		btn5 = types.KeyboardButton('💶 Вартість навчання')
		btn6 = types.KeyboardButton('📚 Програма підготовки')
		btn7 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
		final_message=''

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="Перелік конкурсних предметів"')
		myresult = mycursor.fetchone()
		final_message += ''.join(myresult)
		mycursor.close()
		mydb.close()

	elif get_message_bot == '🗃 Перелік документів':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('📖 Правила прийому')
		btn2 = types.KeyboardButton('🗞 Перелік конкурсних предметів')
		btn3 = types.KeyboardButton('🗃 Перелік документів')
		btn4 = types.KeyboardButton('🧾 Державне замовлення')
		btn5 = types.KeyboardButton('💶 Вартість навчання')
		btn6 = types.KeyboardButton('📚 Програма підготовки')
		btn7 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
		final_message='_Перелік документів вступника:_ \n\n'

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="Перелік документів"')
		myresult = mycursor.fetchone()
		final_message += ''.join(myresult)
		mycursor.close()
		mydb.close()
	
	elif get_message_bot == '⏳ Терміни подачі документів':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('⏳ Терміни подачі документів')
		btn2 = types.KeyboardButton('📆 Розклад вступних випробувань')
		btn3 = types.KeyboardButton('🗳 Результати вступних випробувань')
		btn4 = types.KeyboardButton('📉 Рейтинговий список')
		btn5 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5)
		final_message='_Подача документів:_ \n\n'

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="Подача документів"')
		myresult = mycursor.fetchone()
		final_message += ''.join(myresult)
		mycursor.close()
		mydb.close()

	elif get_message_bot == '📆 Розклад вступних випробувань':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('⏳ Терміни подачі документів')
		btn2 = types.KeyboardButton('📆 Розклад вступних випробувань')
		btn3 = types.KeyboardButton('🗳 Результати вступних випробувань')
		btn4 = types.KeyboardButton('📉 Рейтинговий список')
		btn5 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5)

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="Розклад вступних випробувань"')
		myresult = mycursor.fetchone()
		final_message = ''.join(myresult)
		mycursor.close()
		mydb.close()

	elif get_message_bot == '🗳 Результати вступних випробувань':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('⏳ Терміни подачі документів')
		btn2 = types.KeyboardButton('📆 Розклад вступних випробувань')
		btn3 = types.KeyboardButton('🗳 Результати вступних випробувань')
		btn4 = types.KeyboardButton('📉 Рейтинговий список')
		btn5 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5)

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="Результати вступних випробувань"')
		myresult = mycursor.fetchone()
		final_message = ''.join(myresult)
		mycursor.close()
		mydb.close()

	elif get_message_bot == '📉 Рейтинговий список':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('⏳ Терміни подачі документів')
		btn2 = types.KeyboardButton('📆 Розклад вступних випробувань')
		btn3 = types.KeyboardButton('🗳 Результати вступних випробувань')
		btn4 = types.KeyboardButton('📉 Рейтинговий список')
		btn5 = types.KeyboardButton('🔙 Меню')
		markup.add(btn1, btn2, btn3, btn4, btn5)

		mydb = mysql.connector.connect(host=mHost, user=mUser, password=mPswrd, database=mDb)
		mycursor = mydb.cursor()
		mycursor.execute('SELECT text FROM documents WHERE id="Рейтинговий список"')
		myresult = mycursor.fetchone()
		final_message = ''.join(myresult)
		mycursor.close()
		mydb.close()
	
	elif get_message_bot == '📮 Запитати':
		markup = None
		final_message = "Напишіть ваше питання:"
		bot.register_next_step_handler(message, process_question_step)

	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('🏫 Приймальна комісія')
		btn2 = types.KeyboardButton('🗄 Спеціальності')
		btn3 = types.KeyboardButton('📕 Правила вступної кампанії')
		btn4 = types.KeyboardButton('🗓 Етапи вступної кампанії')
		btn5 = types.KeyboardButton('🚪 День відкритих дверей')
		btn6 = types.KeyboardButton('📝 Підготовчі курси')
		btn7=types.KeyboardButton('❓ Часті запитання')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
		final_message = "Упс! Обери потрібну категорію з меню:"

	if len(final_message) > 4096:
		for x in range(0, len(final_message), 4096):
			bot.send_message(message.chat.id, final_message[x:x+4096], parse_mode="Markdown", reply_markup=markup, disable_web_page_preview=True)
	else:
		bot.send_message(message.chat.id, final_message, parse_mode="Markdown", reply_markup=markup, disable_web_page_preview=True)

bot.polling(none_stop=True)
