import time
import asyncio
import aiohttp
import json
from constants import * # импортируем константы
from loader import bot, DB
from datetime import datetime, timedelta

async def print_tt_for_week(call_message_chat_id, DAYS, PARAS):
	result = await DB.get(call_message_chat_id)
	groupid = result[0][4]
	string = ''
	async with aiohttp.ClientSession() as client:
		r = await client.get(f'https://tt.chuvsu.ru/export/getgroupttweek?user=guest&group={groupid}&week=0')
		r = await r.json(content_type='text/html')
		day_count = 0
		for i in r.keys(): # перебираем все дни из словаря r
			string += f'__________________________________\n{DAYS[day_count]}'
			temp_r = r[i] # временно записываем все пары одного дня
			if temp_r == []:
				string += '\n🙌Выходной\n'
			for j in range(len(temp_r)): # перебираем каждую пару дня отдельно
				begin = int(temp_r[j]['begin'])
				end = int(temp_r[j]['end'])
				if temp_r[j]['dist'] == '1':
					aud = '🖥Дистан.'
				else:
					if {temp_r[j]['type']} == '(лк)':
						aud = f"📖{temp_r[j]['aud']}"
					else:
						aud = f"✏️{temp_r[j]['aud']}"
				if begin != end:
					while begin <= end:
						if bool(temp_r[j]['sub']):
							if result[0][5] == int(temp_r[j]['sub']):
								string += f"\n{PARAS[begin-1]}\n{aud} <b>{temp_r[j]['disc']}</b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n<i>{temp_r[j]['sub']} подгруппа</i>\n"
							elif result[0][5] == 0:
								string += f"\n{PARAS[begin-1]}\n{aud} <b>{temp_r[j]['disc']}</b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n<i>{temp_r[j]['sub']} подгруппа</i>\n"
						else:
							string += f"\n{PARAS[begin-1]}\n{aud} <b>{temp_r[j]['disc']}</b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n"
						begin += 1
				else:
					if bool(temp_r[j]['sub']):
						if result[0][5] == int(temp_r[j]['sub']):
							string += f"\n{PARAS[begin-1]}\n{aud} <b>{temp_r[j]['disc']}</b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n<i>{temp_r[j]['sub']} подгруппа</i>\n"
						elif result[0][5] == 0:
							string += f"\n{PARAS[begin-1]}\n{aud} <b>{temp_r[j]['disc']}</b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n<i>{temp_r[j]['sub']} подгруппа</i>\n"
					else:
						string += f"\n{PARAS[begin-1]}\n{aud} <b>{temp_r[j]['disc']}</b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n"
			day_count += 1
	await bot.send_message(call_message_chat_id, string, disable_web_page_preview = True)

async def print_tt_for_next_week(call_message_chat_id, DAYS, PARAS):
	result = await DB.get(call_message_chat_id)
	groupid = result[0][4]
	string = 'ℹ️РАСПИСАНИЕ НА СЛЕДУЮЩУЮ НЕДЕЛЮℹ️'
	async with aiohttp.ClientSession() as client:
		r = await client.get(f'https://tt.chuvsu.ru/export/getgroupttweek?user=guest&group={groupid}&week=1')
		r = await r.json(content_type='text/html')
		day_count = 0
		for i in r.keys(): # перебираем все дни из словаря r
			string += f'__________________________________\n{DAYS[day_count]}'
			temp_r = r[i] # временно записываем все пары одного дня
			if temp_r == []:
				string += '\n🙌Выходной\n'
			for j in range(len(temp_r)): # перебираем каждую пару дня отдельно
				begin = int(temp_r[j]['begin'])
				end = int(temp_r[j]['end'])
				if temp_r[j]['dist'] == '1':
					aud = '🖥Дистан.'
				else:
					if {temp_r[j]['type']} == '(лк)':
						aud = f"📖{temp_r[j]['aud']}"
					else:
						aud = f"✏️{temp_r[j]['aud']}"
				if begin != end:
					while begin <= end:
						if bool(temp_r[j]['sub']):
							if result[0][5] == int(temp_r[j]['sub']):
								string += f"\n{PARAS[begin-1]}\n{temp_r[j]['aud']} <b>{temp_r[j]['disc']}</b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n<i>{temp_r[j]['sub']} подгруппа</i>\n"
							elif result[0][5] == 0:
								string += f"\n{PARAS[begin-1]}\n{temp_r[j]['aud']} <b>{temp_r[j]['disc']}<b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n<i>{temp_r[j]['sub']} подгруппа</i>\n"
						else:
							string += f"\n{PARAS[begin-1]}\n{temp_r[j]['aud']} <b>{temp_r[j]['disc']}</b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n"
						begin += 1
				else:
					if bool(temp_r[j]['sub']):
						if result[0][5] == int(temp_r[j]['sub']):
							string += f"\n{PARAS[begin-1]}\n{temp_r[j]['aud']} <b>{temp_r[j]['disc']}</b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n<i>{temp_r[j]['sub']} подгруппа</i>\n"
						elif result[0][5] == 0:
							string += f"\n{PARAS[begin-1]}\n{temp_r[j]['aud']} <b>{temp_r[j]['disc']}</b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n<i>{temp_r[j]['sub']} подгруппа</i>\n"
					else:
						string += f"\n{PARAS[begin-1]}\n{temp_r[j]['aud']} <b>{temp_r[j]['disc']}</b> ({temp_r[j]['type']})\n{temp_r[j]['teacher']}\n"
			day_count += 1
	await bot.send_message(call_message_chat_id, string+'\nℹ️РАСПИСАНИЕ НА СЛЕДУЮЩУЮ НЕДЕЛЮℹ️', disable_web_page_preview = True)

async def print_tt_for_tommorow(call_message_chat_id, DAYS, PARAS):
	result = await DB.get(call_message_chat_id)
	groupid = result[0][4]
	string = ''
	async with aiohttp.ClientSession() as client:
		r = await client.get(f'https://tt.chuvsu.ru/export/getgroupttday?user=guest&group={groupid}&day=1')
		r = await r.json(content_type='text/html')
		for i in r.keys():
			r = r[i]
			if r == []:
				string = '🙌Завтра выходной'
			else:
				date_format = '%d.%m.%Y'
				today = datetime.now()
				tomorrow = today + timedelta(days=1)
				string += f"{DAYS[int(time.strftime('%w'))]} | Завтра | <b>{str(tomorrow.strftime(date_format))}</b>\n"
				for j in range(len(r)):
					begin = int(r[j]['begin'])
					end = int(r[j]['end'])
					if r[j]['dist'] == '1':
						aud = '🖥Дистан.'
					else:
						if {r[j]['type']} == '(лк)':
							aud = f"📖{r[j]['aud']}"
						else:
							aud = f"✏️{r[j]['aud']}"
					if begin != end:
						while begin <= end:
							if bool(r[j]['sub']):
								if result[0][5] == int(r[j]['sub']):
									string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n<i>{r[j]['sub']} подгруппа</i>\n"
								elif result[0][5] == 0:
									string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n<i>{r[j]['sub']} подгруппа</i>\n"
							else:
								string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n"
							begin += 1
					else:
						if bool(r[j]['sub']):
							if result[0][5] == int(r[j]['sub']):
								string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n<i>{r[j]['sub']} подгруппа</i>\n"
							elif result[0][5] == 0:
								string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n<i>{r[j]['sub']} подгруппа</i>\n"
						else:
							string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n"
	await bot.send_message(call_message_chat_id, string, disable_web_page_preview = True)

async def print_tt_for_today(call_message_chat_id, DAYS, PARAS):
	result = await DB.get(call_message_chat_id)
	groupid = result[0][4]
	string = ''
	async with aiohttp.ClientSession() as client:
		r = await client.get(f'https://tt.chuvsu.ru/export/getgroupttday?user=guest&group={groupid}&day=0')
		r = await r.json(content_type='text/html')
		for i in r.keys():
			r = r[i]
			if r == []:
				string = '🙌Сегодня выходной'
			else:
				string += f"{DAYS[int(time.strftime('%w'))-1]} | Сегодня | <b>{time.strftime('%d.%m.%y')}</b>\n"
				for j in range(len(r)):
					begin = int(r[j]['begin'])
					end = int(r[j]['end'])
					if r[j]['dist'] == '1':
						aud = '🖥Дистан.'
					else:
						if {r[j]['type']} == '(лк)':
							aud = f"📖{r[j]['aud']}"
						else:
							aud = f"✏️{r[j]['aud']}"
					if begin != end:
						while begin <= end:
							if bool(r[j]['sub']):
								if result[0][5] == int(r[j]['sub']):
									string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n<i>{r[j]['sub']} подгруппа</i>\n"
								elif result[0][5] == 0:
									string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n<i>{r[j]['sub']} подгруппа</i>\n"
							else:
								string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n"
							begin += 1
					else:
						if bool(r[j]['sub']):
							if result[0][5] == int(r[j]['sub']):
								string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n<i>{r[j]['sub']} подгруппа</i>\n"
							elif result[0][5] == 0:
								string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n<i>{r[j]['sub']} подгруппа</i>\n"
						else:
							string += f"\n{PARAS[begin-1]}\n{aud} <b>{r[j]['disc']}</b> ({r[j]['type']})\n{r[j]['teacher']}\n"
	await bot.send_message(call_message_chat_id, string, disable_web_page_preview = True)

async def get_week_info(call_message_chat_id):
	async with aiohttp.ClientSession() as client:
		r = await client.get(f'https://tt.chuvsu.ru/export/getperiod?user=guest')
		r = await r.json(content_type='text/html')
		await bot.send_message(call_message_chat_id, f"Идёт {r['week']} неделя | {r['period']} | {time.strftime('%d.%m.%y')}", disable_web_page_preview = True)

async def get_level(fac_id, form_id):
	async with aiohttp.ClientSession() as client:
		r = await client.get(f'https://tt.chuvsu.ru/export/getlevels?user=guest&fac={fac_id}&fo={form_id}')
		r = await r.json(content_type='text/html')
		return r

async def get_groups_without_course(fac_id, form_id, level_id):
	async with aiohttp.ClientSession() as client:
		r = await client.get(f'https://tt.chuvsu.ru/export/getgroups?user=guest&fac={fac_id}&fo=0&level={level_id}')
		r = await r.json(content_type='text/html')
		r = r[fac_id][form_id][level_id]
		return r

async def get_groups(fac_id, form_id, level_id, course):
	async with aiohttp.ClientSession() as client:
		r = await client.get(f'https://tt.chuvsu.ru/export/getgroups?user=guest&fac={fac_id}&fo=0&level={level_id}')
		r = await r.json(content_type='text/html')
		r = r[fac_id][form_id][level_id][course]
		return r

async def get_groupname(groupid):
	async with aiohttp.ClientSession() as client:
		r = await client.get(f'https://tt.chuvsu.ru/export/getgroupinfo?user=guest&gid={groupid}')
		r = await r.json(content_type='text/html')
		r = r['name']
		return r


