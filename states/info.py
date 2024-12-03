from aiogram.dispatcher.filters.state import StatesGroup, State

class Info(StatesGroup):
	
	# Выбор ВУЗа
	vuz = State()
	
	# ЧГУ
	chuvsu_what = State()
	chuvsu_add_fac = State()
	chuvsu_add_form = State()
	chuvsu_add_level = State()
	chuvsu_add_course = State()
	chuvsu_add_group_with_button = State()
	chuvsu_add_group = State()
	chuvsu_add_subgroup = State()
	
	# ЧГАУ
	chgau_what = State()
	chgau_add_fac = State()
	chgau_add_course = State()
	chgau_add_group = State()
	
	# Статус замены ВУЗа или группы
	update = State()