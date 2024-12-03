from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Перезапуск"),
            types.BotCommand("settings", "Поменять группу или подгруппу"),
            types.BotCommand("help", "Помощь"),
            types.BotCommand("weekinfo", "Какая неделя идет"),
            types.BotCommand("nextweek", "Расписание на след. неделю")
        ]
    )