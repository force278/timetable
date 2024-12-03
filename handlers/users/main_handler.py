import random
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.builtin import CommandSettings
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from states.info import Info
from loader import dp, DB, bot, CR
from constants import *
from funcs.chuvsu_func import *
from funcs.chgau_func import *

count_of_distribution = 0
count_of_ban = 0

# НАЖАЛИ СТАРТ
@dp.message_handler(CommandStart())
async def start_command(message: types.Message):
	await DB.add(message.from_user.id)
	await CR.augment()
	await DB.update(UserID=message.from_user.id, University='ЧГУ')
	keyboard = types.InlineKeyboardMarkup()
	key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button') 
	keyboard.add(key_button)
	await bot.send_message(message.from_user.id, text='🕊️Привет, я умею показывать расписание.\n1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры 💻\n🔹Например: <b>ивт-42-20</b>\n\n2️⃣Выбрать группу кнопками 📲', reply_markup=keyboard)
	await Info.chuvsu_what.set()


# НАЖАЛИ КАКАЯ НЕДЕЛЯ 
@dp.message_handler(commands=['weekinfo'])
async def weekinfo_command(message: types.Message):
	await get_week_info(message.from_user.id)
	await CR.augment()


# НАЖАЛИ СЛЕДУЮЩАЯ НЕДЕЛЯ
@dp.message_handler(commands=['nextweek'])
async def weekinfo_command(message: types.Message):
	result = await DB.get(message.from_user.id)
	await CR.augment()
	if result[0][2] == 'ЧГАУ':
		await bot.send_message(message.from_user.id, text='Для ЧГАУ эта функция пока не доступна')
	else:
		await bot.send_message(message.from_user.id, text='🔄Получаю данные...')
		await print_tt_for_next_week(message.from_user.id, DAYS, PARAS)
		await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)


@dp.message_handler(commands=['i'])
async def weekinfo_command(message: types.Message):
	result = await DB.info()
	string = await CR.get_info()
	await bot.send_message(message.from_user.id, text= f'Ботом пользуется: {result[0]} 👨‍🎓\nИз них\n🔵ЧГУ: <code>{result[1]}</code>\n🟢ЧГАУ: <code>{result[2]}</code>\n\n{string}')


# НАЖАЛИ НАСТРОЙКИ
@dp.message_handler(CommandSettings())
async def settings(message):
	vuz = await DB.get(message.from_user.id)
	vuz = vuz[0][2]
	await CR.augment()
	if vuz == 'ЧГАУ':
		keyboard = types.InlineKeyboardMarkup()
		key_group_edit = types.InlineKeyboardButton(text='Изменить группу', callback_data='group_edit')
		key_close = types.InlineKeyboardButton(text='❌Закрыть', callback_data='close')
		keyboard.add(key_group_edit)
		keyboard.add(key_close)
		result = await DB.get(message.from_user.id)
		temp = f'Ваша текущая группа: {result[0][3]}\n\n'
		await Info.update.set()
		await bot.send_message(message.from_user.id, text= temp+'Что хотите изменить?', reply_markup=keyboard)
	else:
		keyboard = types.InlineKeyboardMarkup()
		key_group_edit = types.InlineKeyboardButton(text='Изменить группу', callback_data='group_edit')
		key_subgroup_edit = types.InlineKeyboardButton(text='Изменить подгруппу', callback_data='subgroup_edit')
		key_close = types.InlineKeyboardButton(text='❌Закрыть', callback_data='close')
		keyboard.add(key_group_edit, key_subgroup_edit)
		keyboard.add(key_close)
		result = await DB.get(message.from_user.id)
		temp = f'Ваша текущая группа: {result[0][3]}\nПодгруппа: {result[0][5]}\n\n'
		await Info.update.set()
		await bot.send_message(message.from_user.id, text= temp+'Что хотите изменить?', reply_markup=keyboard)

# НАЖАЛИ ПОМОЩЬ
@dp.message_handler(CommandHelp())
async def _help(message):
	await CR.augment()
	await bot.send_message(message.from_user.id, text= 'Нашел ошибку?\nСообщи <a href="https://t.me/weekendend">мне</a> о ней.', disable_web_page_preview=True)

# НАЖАЛИ ЧТО-ТО ИЗ ПУНКТА МЕНЮ
@dp.callback_query_handler(state=Info.update)
async def update(call: types.CallbackQuery, state=FSMContext):
	await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	await CR.augment()
	vuz = await DB.get(call.message.chat.id)
	vuz = vuz[0][2]
	if vuz == 'ЧГАУ':
		if call.data == 'group_edit':
			keyboard = types.InlineKeyboardMarkup()
			key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button')
			keyboard.add(key_button)
			await bot.send_message(call.message.chat.id, text='1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры.\nНапример: <b>а-1м</b>\n\n2️⃣Выбрать группу кнопками.', reply_markup=keyboard)
			await Info.chgau_what.set()
		elif call.data == 'close':
			await state.finish()
			await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	else:
		if call.data == 'group_edit':
			keyboard = types.InlineKeyboardMarkup()
			key_button = types.InlineKeyboardButton(text='Выбрать группу кнопками', callback_data='button')
			keyboard.add(key_button)
			await bot.send_message(call.message.chat.id, text='1️⃣Ты можешь прямо сейчас ввести название группы с клавиатуры.\nНапример: ивт-42-20\n\n2️⃣Выбрать группу кнопками.', reply_markup=keyboard)
			await Info.chuvsu_what.set()
		elif call.data == 'subgroup_edit':
			temp = ''
			result = await DB.get(call.message.chat.id)
			if len(result) == 0:
				DB.add(call.message.chat.id)
			else:
				if result[0][5] == 0:
					temp = 'ℹ️Вы без подгруппы\n\n'
				else:
					temp = 'ℹ️Текущий: ' + str(result[0][5]) + ' подгруппа\n\n'
			keyboard = types.InlineKeyboardMarkup()
			key_nosubroup = types.InlineKeyboardButton(text='без подгруппы', callback_data='nosubgroup')
			keyboard.add(key_nosubroup)
			key_subgroup1 = types.InlineKeyboardButton(text='1 подгруппа', callback_data='subgroup1')
			keyboard.add(key_subgroup1)
			key_subgroup2 = types.InlineKeyboardButton(text='2 подгруппа', callback_data='subgroup2')
			keyboard.add(key_subgroup2)
			key_close = types.InlineKeyboardButton(text='❌Отменить', callback_data='close')
			keyboard.add(key_close)
			await Info.chuvsu_add_subgroup.set()
			await bot.send_message(call.message.chat.id, text= temp +'Из какой Вы подгруппы?', reply_markup=keyboard)
		elif call.data == 'close':
			await state.finish()
			await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

@dp.message_handler(state=Info.update)
async def update(message):
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
		
# НАПИСАЛИ ТЕКСТ БЕЗ СТАТУСА
@dp.message_handler(content_types=['text'])
async def message(message: types.Message):
	result = await DB.get(message.from_user.id)
	if message.text.lower() == 'расписание на неделю':
		await bot.send_message(message.from_user.id, text='🔄Получаю данные...')
		if result[0][2] == 'ЧГАУ':
			await CR.augment()
			await bot.send_message(call.message.chat.id, text= temp +'Для ЧГАУ эта функция пока недоступна.', reply_markup=keyboard)
		else:
			await CR.chuvsu_augment()
			await print_tt_for_week(message.from_user.id, DAYS, PARAS)
		await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)
	elif (message.text).lower() == 'завтра':
		await bot.send_message(message.from_user.id, text='🔄Получаю данные...')
		if result[0][2] == 'ЧГАУ':
			await CR.chgau_augment()
			await chgau_print_tt_for_tomorrow(message.from_user.id)
		else:
			await CR.chuvsu_augment()
			await print_tt_for_tommorow(message.from_user.id, DAYS, PARAS)
		await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)
	elif (message.text).lower() == 'сегодня':
		await bot.send_message(message.from_user.id, text='🔄Получаю данные...')
		if result[0][2] == 'ЧГАУ':
			await CR.chgau_augment()
			await chgau_print_tt_for_today(message.from_user.id)
		else:
			await CR.chuvsu_augment()
			await print_tt_for_today(message.from_user.id, DAYS, PARAS)
		await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)
	elif (message.text).lower() == 'рассылка!':
		await bot.send_message(message.from_user.id, text='🔄Отправляю...')
		result = await DB.get_all_usersid()
		for i in result:
			try:
				await bot.send_message(i[0], text='''Доброго времени, дорогие друзья. Спешим сообщить, что бот обновлен и снова работает.

Так же, рекомендуем вам приложение «Мой ЧувГУ» от команды факультета ИВТ, там тоже можно смотреть расписание. 
Скачать можно здесь: https://online.chuvsu.ru/download

Успехов вам в учебном году.''')
				count_of_distribution = count_of_distribution + 1
			except:
				pass
		await bot.send_message(message.from_user.id, text=f'Количество пользователей получивших рассылку {count_of_distribution}\n\nНе получивших {count_of_ban}')
		
	else:
		await CR.augment()
		await bot.send_sticker(chat_id=message.from_user.id, sticker=stickers['dont_understand'][random.randint(0,2)])
		await bot.send_message(message.from_user.id, text='🤷Не знаю что ответить.')
