from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from states.info import Info
from loader import dp, DB, bot, CR
from constants import *
from funcs.chgau_func import *

# ВЫБРАЛИ ЧГАУ КНОПКАМИ (ПОКАЗЫВАЕМ ФАКУЛЬТЕТЫ)
@dp.callback_query_handler(state=Info.chgau_what)
async def chgau_what(call: types.CallbackQuery, state=FSMContext):
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await CR.chgau_augment()
	if call.data == 'button':
		keyboard = types.InlineKeyboardMarkup()
		for num, fac in CHGAU_FAC.items():
			key_fac_edit = types.InlineKeyboardButton(text=fac['name'], callback_data=num)
			keyboard.add(key_fac_edit)
		key_form_edit = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_form_edit)
		await bot.send_message(call.message.chat.id, text='Из какого Вы факультета?', reply_markup=keyboard)
		await Info.chgau_add_fac.set()
	elif call.data == 'back':
		await DB.update(UserID=message.from_user.id, University='ЧГУ')
		keyboard = types.InlineKeyboardMarkup()
		key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button') 
		keyboard.add(key_button)
		await bot.send_message(message.from_user.id, text='🕊️Привет, я умею показывать расписание.\n1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры 💻\n🔹Например: <b>ивт-42-20</b>\n\n2️⃣Выбрать группу кнопками 📲', reply_markup=keyboard)
		await Info.chuvsu_what.set()


# ВЫБРАЛИ ТЕКСТОМ
@dp.message_handler(state=Info.chgau_what)
async def chgau_what(message: types.Message, state=FSMContext):
	# await bot.delete_message(chat_id=message.from_user.id, message_id=message.from_user.id)
	await CR.chgau_augment()
	if message.text.lower() in CHGAU_GROUPS:
		await DB.update(UserID=message.from_user.id, GroupID=CHGAU_GROUPS[message.text.lower()]['groupid'], GroupName=message.text.lower())
		keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row('Завтра', 'Сегодня')
		await state.finish()
		await bot.send_message(message.from_user.id, text=f'✅Теперь Вы в группе: {message.text.lower()}' , reply_markup=keyboard)
	elif message.text.lower() == '/start':
		await DB.update(UserID=message.from_user.id, University='ЧГУ')
		keyboard = types.InlineKeyboardMarkup()
		key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button') 
		keyboard.add(key_button)
		await bot.send_message(message.from_user.id, text='🕊️Привет, я умею показывать расписание.\n1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры 💻\n🔹Например: <b>ивт-42-20</b>\n\n2️⃣Выбрать группу кнопками 📲', reply_markup=keyboard)
		await Info.chuvsu_what.set()
	else:
		await bot.send_message(message.from_user.id, text=f'🤷Не знаю такую группу.\n\nВведи название группы так же\nкак на сайте расписания.')



# ВЫБРАЛИ ФАКУЛЬТЕТ (ПОКАЗЫВАЕМ КУРС)
@dp.callback_query_handler(state=Info.chgau_add_fac)
async def chgau_add_fac(call: types.CallbackQuery, state=FSMContext):
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await CR.chgau_augment()
	if call.data == 'back':
		await DB.update(UserID=message.from_user.id, University='ЧГУ')
		keyboard = types.InlineKeyboardMarkup()
		key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button') 
		keyboard.add(key_button)
		await bot.send_message(call.message.chat.id, text='1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры 💻\n🔹Например: <b>а-1м</b>\n\n2️⃣Выбрать группу кнопками 📲', reply_markup=keyboard)
		await Info.chgau_what.set()
	else:
		await state.update_data(fac_id = call.data)
		keyboard = types.InlineKeyboardMarkup()
		course = CHGAU_COURSE[call.data]
		for i in range(1, int(course)+1):
			key_course = types.InlineKeyboardButton(text=f'{i} курс', callback_data=i)
			keyboard.insert(key_course)
		key_form_edit = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_form_edit)
		await bot.send_message(call.message.chat.id, text='Выберите курс', reply_markup=keyboard)
		await Info.chgau_add_course.set()

@dp.message_handler(state=Info.chgau_add_fac)
async def chgau_add_fac(message):
	await CR.augment()
	if message.text.lower() == '/start':
		await DB.update(UserID=message.from_user.id, University='ЧГУ')
		keyboard = types.InlineKeyboardMarkup()
		key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button') 
		keyboard.add(key_button)
		await bot.send_message(message.from_user.id, text='🕊️Привет, я умею показывать расписание.\n1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры 💻\n🔹Например: <b>ивт-42-20</b>\n\n2️⃣Выбрать группу кнопками 📲', reply_markup=keyboard)
		await Info.chuvsu_what.set()
	else:
		await bot.send_message(message.from_user.id, text='👆Жду ответа на вопрос выше.')  


# ВЫБРАЛИ КУРС (ПОКАЗЫВАЕМ ГРУППЫ)
@dp.callback_query_handler(state=Info.chgau_add_course)
async def chgau_add_course(call: types.CallbackQuery, state=FSMContext):
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await CR.chgau_augment()
	if call.data == 'back':
		keyboard = types.InlineKeyboardMarkup()
		for num, fac in CHGAU_FAC.items():
			key_fac_edit = types.InlineKeyboardButton(text=fac['name'], callback_data=num)
			keyboard.add(key_fac_edit)
		key_form_edit = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_form_edit)
		await bot.send_message(call.message.chat.id, text='Из какого Вы факультета?', reply_markup=keyboard)
		await Info.chgau_add_fac.set()
	else:
		data = await state.get_data()
		data = data['fac_id']
		data = CHGAU_FAC[data]['groups']['course'][call.data]
		keyboard = types.InlineKeyboardMarkup()
		for key, value in data.items():
			key_group = types.InlineKeyboardButton(text=key, callback_data=data[key]['groupid'])
			keyboard.add(key_group)
		key_form_edit = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_form_edit)
		await bot.send_message(call.message.chat.id, text='Из какой Вы группы?', reply_markup=keyboard)
		await Info.chgau_add_group.set()

@dp.message_handler(state=Info.chgau_add_course)
async def chgau_add_course(message):
	await CR.augment()
	if message.text.lower() == '/start':
		await DB.update(UserID=message.from_user.id, University='ЧГУ')
		keyboard = types.InlineKeyboardMarkup()
		key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button') 
		keyboard.add(key_button)
		await bot.send_message(message.from_user.id, text='🕊️Привет, я умею показывать расписание.\n1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры 💻\n🔹Например: <b>ивт-42-20</b>\n\n2️⃣Выбрать группу кнопками 📲', reply_markup=keyboard)
		await Info.chuvsu_what.set()
	else:
		await bot.send_message(message.from_user.id, text='👆Жду ответа на вопрос выше.')  


# ВЫБРАЛИ ГРУППУ 
@dp.callback_query_handler(state=Info.chgau_add_group)
async def chgau_add_group(call: types.CallbackQuery, state=FSMContext):
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await CR.chgau_augment()
	if call.data == 'back':
		data = await state.get_data()
		data = data['fac_id']
		course = CHGAU_COURSE[data]
		keyboard = types.InlineKeyboardMarkup()
		for i in range(1, int(course)+1):
			key_course = types.InlineKeyboardButton(text=f'{i} курс', callback_data=i)
			keyboard.insert(key_course)
		key_form_edit = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_form_edit)
		await bot.send_message(call.message.chat.id, text='Выберите курс', reply_markup=keyboard)
		await Info.chgau_add_course.set()
	else:
		data = await state.get_data()
		data = data['fac_id']
		groupname = CHGAU_GROUPS_INV[data][call.data]
		keyboard = types.InlineKeyboardMarkup()
		keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row('Завтра', 'Сегодня')
		await DB.update(UserID=call.message.chat.id, GroupID=call.data, GroupName=groupname)
		await state.finish()
		await bot.send_message(call.message.chat.id, text=f'✅Теперь Вы в группе {groupname}', reply_markup=keyboard)
	
@dp.message_handler(state=Info.chgau_add_group)
async def chgau_add_group(message):
	await CR.augment()
	if message.text.lower() == '/start':
		await DB.update(UserID=message.from_user.id, University='ЧГУ')
		keyboard = types.InlineKeyboardMarkup()
		key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button') 
		keyboard.add(key_button)
		await bot.send_message(message.from_user.id, text='🕊️Привет, я умею показывать расписание.\n1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры 💻\n🔹Например: <b>ивт-42-20</b>\n\n2️⃣Выбрать группу кнопками 📲', reply_markup=keyboard)
		await Info.chuvsu_what.set()
	else:
		await bot.send_message(message.from_user.id, text='👆Жду ответа на вопрос выше.')  
