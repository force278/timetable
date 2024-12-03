import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from states.info import Info
from loader import dp, DB, bot, CR
from constants import *
from funcs.chuvsu_func import *


# ВЫБРАЛИ ЧГУ И ХОТЯТ ВЫБРАТЬ ГРУППУ КНОПКАМИ (ПОКАЗЫВАЕМ ФАКУЛЬТЕТЫ)
@dp.callback_query_handler(state=Info.chuvsu_what)
async def chuvsu_what(call: types.CallbackQuery, state=FSMContext):
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await CR.chuvsu_augment()
	if call.data == 'button':
		keyboard = types.InlineKeyboardMarkup()
		for key, value in FAC.items():
			key_fac_edit = types.InlineKeyboardButton(text=value, callback_data=key)
			keyboard.add(key_fac_edit)
		key_form_edit = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_form_edit)
		await bot.send_message(call.message.chat.id, text='Из какого Вы факультета?', reply_markup=keyboard)
		await Info.chuvsu_add_fac.set()
	elif call.data == 'back': # ЕСЛИ ХОТЯТ ВЕРНУТЬСЯ К ВЫБОРУ ВУЗа
		await DB.update(UserID=message.from_user.id, University='ЧГУ')
		keyboard = types.InlineKeyboardMarkup()
		key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button') 
		keyboard.add(key_button)
		await bot.send_message(message.from_user.id, text='🕊️Привет, я умею показывать расписание.\n1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры 💻\n🔹Например: <b>ивт-42-20</b>\n\n2️⃣Выбрать группу кнопками 📲', reply_markup=keyboard)
		await Info.chuvsu_what.set()


# ВЫБРАЛИ ЧГУ И НАПИСАЛИ ТЕКСТОМ (ХОТЯТ ВЫБРАТЬ ГРУППУ ТЕКСТОМ)
@dp.message_handler(state=Info.chuvsu_what)
async def chuvsu_what(message: types.Message, state=FSMContext):
	await CR.chuvsu_augment()
	if message.text.lower() in GROUPS:
		await DB.update(UserID=message.from_user.id, GroupID=GROUPS[message.text.lower()], GroupName=message.text.lower())
		keyboard = types.InlineKeyboardMarkup()
		key_nosubroup = types.InlineKeyboardButton(text='без подгруппы', callback_data='nosubgroup')
		keyboard.add(key_nosubroup)
		key_subgroup1 = types.InlineKeyboardButton(text='1 подгруппа', callback_data='subgroup1')
		key_subgroup2 = types.InlineKeyboardButton(text='2 подгруппа', callback_data='subgroup2')
		keyboard.add(key_subgroup1, key_subgroup2)
		await Info.chuvsu_add_subgroup.set()
		await bot.send_message(message.from_user.id, text=f'✅Теперь Вы в группе: {message.text.lower()}\n\nИз какой Вы подгруппы?' , reply_markup=keyboard)
	elif message.text.lower() == '/start':
		await DB.update(UserID=message.from_user.id, University='ЧГУ')
		keyboard = types.InlineKeyboardMarkup()
		key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button') 
		keyboard.add(key_button)
		await bot.send_message(message.from_user.id, text='🕊️Привет, я умею показывать расписание.\n1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры 💻\n🔹Например: <b>ивт-42-20</b>\n\n2️⃣Выбрать группу кнопками 📲', reply_markup=keyboard)
		await Info.chuvsu_what.set()
	else:
		await bot.send_message(message.from_user.id, text=f'🤷Не знаю такую группу.\n\nВведи название группы так же\nкак на сайте расписания.')

# ВЫБРАЛИ ФАКУЛЬТЕТ (ПОКАЗЫВАЕМ ФОРМЫ ОБУЧЕНИЯ)
@dp.callback_query_handler(state=Info.chuvsu_add_fac)
async def add_fac(call: types.CallbackQuery, state=FSMContext):
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await CR.chuvsu_augment()
	if call.data == 'back':
		keyboard = types.InlineKeyboardMarkup()
		key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button') 
		keyboard.add(key_button)
		await bot.send_message(call.message.chat.id, text='1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры 💻\n🔹Например: <b>ивт-42-20</b>\n\n2️⃣Выбрать группу кнопками 📲', reply_markup=keyboard)
		await Info.chuvsu_what.set()
	else:
		await state.update_data(fac_id = call.data)
		keyboard = types.InlineKeyboardMarkup()
		key_form_edit = types.InlineKeyboardButton(text='Очная', callback_data='1')
		keyboard.add(key_form_edit)
		key_form_edit = types.InlineKeyboardButton(text='Очно-заочная', callback_data='2')
		keyboard.add(key_form_edit)
		key_form_edit = types.InlineKeyboardButton(text='Заочная', callback_data='3')
		keyboard.add(key_form_edit)
		key_back = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_back)
		await bot.send_message(call.message.chat.id, text='Выберите Вашу форму обучения:', reply_markup=keyboard)
		await Info.chuvsu_add_form.set()

@dp.message_handler(state=Info.chuvsu_add_fac)
async def chuvsu_add_fac(message):
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


# ВЫБРАЛИ ФОРМУ ОБУЧЕНИЯ (ПОКАЗЫВАЕМ УРОВНИ ОБРАЗОВАНИЯ)
@dp.callback_query_handler(state=Info.chuvsu_add_form)
async def add_form(call: types.CallbackQuery, state=FSMContext):
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await CR.chuvsu_augment()
	if call.data == 'back':
		keyboard = types.InlineKeyboardMarkup()
		for key, value in FAC.items():
			key_fac_edit = types.InlineKeyboardButton(text=value, callback_data=key)
			keyboard.add(key_fac_edit)
		key_form_edit = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_form_edit)
		await bot.send_message(call.message.chat.id, text='Из какого Вы факультета?', reply_markup=keyboard)
		await Info.chuvsu_add_fac.set()
	else:
		await state.update_data(form_id = call.data)
		data = await state.get_data()
		levels = await get_level(data['fac_id'], call.data)
		keyboard = types.InlineKeyboardMarkup()
		for key, value in levels.items():
			key_level_edit = types.InlineKeyboardButton(text=value, callback_data=key)
			keyboard.add(key_level_edit)
		key_form_edit = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_form_edit)
		await bot.send_message(call.message.chat.id, text='Выберите Ваш уровень образования:', reply_markup=keyboard)
		await Info.chuvsu_add_level.set()

@dp.message_handler(state=Info.chuvsu_add_form)
async def chuvsu_add_form(message):
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


# ВЫБРАЛИ УРОВЕНЬ ОБРАЗОВАНИЯ (ПОКАЗЫВАЕМ КУРСЫ)
@dp.callback_query_handler(state=Info.chuvsu_add_level)
async def add_level(call: types.CallbackQuery, state=FSMContext):
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await CR.chuvsu_augment()
	if call.data == 'back':
		keyboard = types.InlineKeyboardMarkup()
		key_form_edit = types.InlineKeyboardButton(text='Очная', callback_data='1')
		keyboard.add(key_form_edit)
		key_form_edit = types.InlineKeyboardButton(text='Очно-заочная', callback_data='2')
		keyboard.add(key_form_edit)
		key_form_edit = types.InlineKeyboardButton(text='Заочная', callback_data='3')
		keyboard.add(key_form_edit)
		key_form_edit = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_form_edit)
		await Info.chuvsu_add_form.set()
		await bot.send_message(call.message.chat.id, text='Выберите Вашу форму обучения:', reply_markup=keyboard)
	else:
		await state.update_data(level_id = call.data)
		data = await state.get_data()
		groups = await get_groups_without_course(data['fac_id'], data['form_id'], call.data)
		keyboard = types.InlineKeyboardMarkup()
		i = 0
		for key, value in groups.items():
			i = i + 1
			key_course_edit = types.InlineKeyboardButton(text=f'{str(i)} курс', callback_data=str(i))
			keyboard.insert(key_course_edit)
		key_back = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_back)
		await Info.chuvsu_add_course.set()
		await bot.send_message(call.message.chat.id, text='Выберите Ваш курс:', reply_markup=keyboard)

@dp.message_handler(state=Info.chuvsu_add_level)
async def chuvsu_add_level(message):
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
@dp.callback_query_handler(state=Info.chuvsu_add_course)
async def add_course(call: types.CallbackQuery, state=FSMContext):
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await CR.chuvsu_augment()
	if call.data == 'back':
		data = await state.get_data()
		levels = await get_level(data['fac_id'], data['form_id'])
		keyboard = types.InlineKeyboardMarkup()
		for key, value in levels.items():
			key_level_edit = types.InlineKeyboardButton(text=value, callback_data=key)
			keyboard.add(key_level_edit)
		key_form_edit = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_form_edit)
		await bot.send_message(call.message.chat.id, text='Выберите Ваш уровень образования:', reply_markup=keyboard)
		await Info.chuvsu_add_level.set()
	else:
		await state.update_data(course = call.data)
		data = await state.get_data()
		groups = await get_groups(data['fac_id'], data['form_id'], data['level_id'], call.data)
		keyboard = types.InlineKeyboardMarkup()
		for key, value in groups.items():
			key_group_edit = types.InlineKeyboardButton(text=value, callback_data=key)
			keyboard.add(key_group_edit)
		key_back = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_back)
		await Info.chuvsu_add_group_with_button.set()
		await bot.send_message(call.message.chat.id, text='Выберите Вашу группу:', reply_markup=keyboard)

@dp.message_handler(state=Info.chuvsu_add_course)
async def chuvsu_add_course(message):
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


# ВЫБРАЛИ ГРУППУ (ПОКАЗЫВАЕМ ПОДГРУППЫ)
@dp.callback_query_handler(state=Info.chuvsu_add_group_with_button)
async def add_group_with_button(call: types.CallbackQuery, state=FSMContext):
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await CR.chuvsu_augment()
	if call.data == 'back':
		data = await state.get_data()
		groups = await get_groups_without_course(data['fac_id'], data['form_id'], data['level_id'])
		keyboard = types.InlineKeyboardMarkup()
		i = 0
		for key, value in groups.items():
			i = i + 1
			key_course_edit = types.InlineKeyboardButton(text=f'{str(i)} курс', callback_data=str(i))
			keyboard.insert(key_course_edit)
		key_back = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
		keyboard.add(key_back)
		await Info.chuvsu_add_course.set()
		await bot.send_message(call.message.chat.id, text='Выберите Ваш курс:', reply_markup=keyboard)
	else: 
		groupname = await get_groupname(call.data)
		await state.update_data(group_id = call.data, group_name = groupname)
		await DB.update(UserID=call.message.chat.id, GroupID=call.data, GroupName=groupname)
		keyboard = types.InlineKeyboardMarkup()
		key_nosubroup = types.InlineKeyboardButton(text='без подгруппы', callback_data='nosubgroup')
		keyboard.add(key_nosubroup)
		key_subgroup1 = types.InlineKeyboardButton(text='1 подгруппа', callback_data='subgroup1')
		key_subgroup2 = types.InlineKeyboardButton(text='2 подгруппа', callback_data='subgroup2')
		keyboard.add(key_subgroup1, key_subgroup2)
		await Info.chuvsu_add_subgroup.set()
		await bot.send_message(call.message.chat.id, text=f'✅Теперь Вы в группе: {groupname}\n\nИз какой Вы подгруппы?' , reply_markup=keyboard)


@dp.message_handler(state=Info.chuvsu_add_group_with_button)
async def chuvsu_add_group_with_button(message):
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


# ВЫБРАЛИ ПОДГРУППУ (ГОТОВЫ ПОКАЗЫВАТЬ РАСПИСАНИЕ)
@dp.callback_query_handler(state=Info.chuvsu_add_subgroup)
async def add_subgroup(call: types.CallbackQuery, state=FSMContext):
	await CR.chuvsu_augment()
	if call.data == 'nosubgroup':
		await DB.update(UserID=call.message.chat.id, Subgroup='0')
		await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row('Расписание на неделю', 'Завтра', 'Сегодня')
		await state.finish()
		await bot.send_message(call.message.chat.id, text='✅Теперь Вы без подгруппы', reply_markup=keyboard)
	elif call.data == 'subgroup1':
		await DB.update(UserID=call.message.chat.id, Subgroup='1')
		await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row('Расписание на неделю', 'Завтра', 'Сегодня')
		await state.finish()
		await bot.send_message(call.message.chat.id, text='✅Теперь Вы в 1 подгруппе', reply_markup=keyboard)
	elif call.data == 'subgroup2':
		await DB.update(UserID=call.message.chat.id, Subgroup='2')
		await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row('Расписание на неделю', 'Завтра', 'Сегодня')
		await state.finish()
		await bot.send_message(call.message.chat.id, text='✅Теперь Вы во 2 подгруппе', reply_markup=keyboard)
	elif call.data == 'close':
		await state.finish()
		await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

@dp.message_handler(state=Info.chuvsu_add_subgroup)
async def chuvsu_add_subgroup(message):
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
