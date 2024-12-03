import time
import asyncio
import aiohttp
import json
import re
from constants import * # импортируем константы
from loader import bot, DB, CR
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


MONTH = {'january':'января','february':'февраля','march':'марта','april':'апреля','may':'мая','june':'июня','july':'июля','august':'августа','september':'сентября','october':'октября','november':'ноября','december':'декабря'}


async def chgau_print_tt_for_today(call_message_chat_id):
	result = await DB.get(call_message_chat_id)
	groupname = result[0][3]
	groupid = result[0][4]
	fac = CHGAU_GROUPS[groupname]['url']
	string = ''
	date_format = '%d'
	today = datetime.now()
	month = today.strftime("%B")
	month = MONTH[month.lower()]
	j = 0
	async with aiohttp.ClientSession() as client:
		r = await client.get(f'http://raspis.academy21.ru/data/{fac}/DO/{groupid}.html')
		r = await r.text()
		soup = BeautifulSoup(r, 'lxml')
		string = ''
		for tag in soup.find_all(string=re.compile(today.strftime(date_format) + f'  {month}')):
			temp = tag.parent.parent.parent.parent.parent.parent
			try:
				x = temp.find_all('td')
			except:
				string = '🌄 Сегодня выходной'
				break
			for y in range(len(x)):
				if x[y].get_text().rstrip():
					m = x[y].get_text().strip('\n')
					if y != 0:
						string = string + PARAS_CHGAU[y-1]
					if 'пр' in m[0:3]:
						string = string + '\n✏️' + f'<b>{m}</b>\n\n'
					elif 'л.' in m[0:3]:
						string = string + '\n🎧' + f'<b>{m}</b>\n\n'
					elif 'лаб.' in m[0:5]:
						string = string + '\n✏️' + f'<b>{m}</b>\n\n'
					else:
						string = string + f'<b>{x[y].get_text()}</b>\n\n'
				else:
					j = j + 1
	if j == 7:
		string = string + '🌄 Выходной'
	await bot.send_message(call_message_chat_id, string, disable_web_page_preview = True)


async def chgau_print_tt_for_tomorrow(call_message_chat_id):
	result = await DB.get(call_message_chat_id)
	groupname = result[0][3]
	groupid = result[0][4]
	fac = CHGAU_GROUPS[groupname]['url']
	string = ''
	date_format = '%d'
	today = datetime.now()
	tomorrow = today + timedelta(days=1)
	month = tomorrow.strftime("%B")
	month = MONTH[month.lower()]
	j = 0
	async with aiohttp.ClientSession() as client:
		r = await client.get(f'http://raspis.academy21.ru/data/{fac}/DO/{groupid}.html')
		r = await r.text()
		soup = BeautifulSoup(r, 'lxml')
		string = ''
		for tag in soup.find_all(string=re.compile(tomorrow.strftime(date_format) + f'  {month}')):
			temp = tag.parent.parent.parent.parent.parent.parent
			try:
				x = temp.find_all('td')
			except:
				string = '🌄 Сегодня выходной'
				break
			for y in range(len(x)):
				if x[y].get_text().rstrip():
					m = x[y].get_text().strip('\n')
					if y != 0:
						string = string + PARAS_CHGAU[y-1]
					if 'пр' in m[0:3]:
						string = string + '\n✏️' + f'<b>{m}</b>\n\n'
					elif 'л.' in m[0:3]:
						string = string + '\n🎧' + f'<b>{m}</b>\n\n'
					elif 'лаб.' in m[0:5]:
						string = string + '\n✏️' + f'<b>{m}</b>\n\n'
					else:
						string = string + f'<b>{x[y].get_text()}</b>\n\n'
				else:
					j = j + 1
	if j == 7:
		string = string + '🌄 Выходной'
	await bot.send_message(call_message_chat_id, string, disable_web_page_preview = True)


# async def chgau_print_tt_for_week(call_message_chat_id):
# 	result = await DB.get(call_message_chat_id)
# 	groupname = result[0][3]
# 	groupid = result[0][4]
# 	fac = CHGAU_GROUPS[groupname]['url']
# 	string = ''
# 	date_format = '%d'
# 	temp_day = datetime.now()
# 	async with aiohttp.ClientSession() as client:
# 		r = await client.get(f'http://raspis.academy21.ru/data/{fac}/DO/{groupid}.html')
# 		r = await r.text()
# 		soup = BeautifulSoup(r, 'lxml')
# 		string = ''
# 		for i in range(7):
# 			print(temp_day.strftime(date_format))
# 			for tag in soup.find_all(string=re.compile(temp_day.strftime(date_format))):
# 				temp = tag.parent.parent.parent.parent.parent.parent
# 				try:
# 					x = temp.find_all('td')
# 					for y in range(len(x)):
# 						if x[y].get_text().rstrip():
# 							if y != 0:
# 								string = string + PARAS_CHGAU[y-1]
# 							string = string + x[y].get_text() + '\n\n'
# 				except:
# 					break
# 			y = 0
# 			string = string + '\n\n\n'
# 			temp_day = temp_day + timedelta(days=1)
# 	await bot.send_message(call_message_chat_id, string, disable_web_page_preview = True)