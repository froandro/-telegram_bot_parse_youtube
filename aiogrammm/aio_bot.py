#   Copyright (c) 2022. Сделано мной !!!

import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot.api import TelegramAPIServer
from aiogram.dispatcher import filters
from aiogram.types import InputFile

import commands
import db_sql
import yotube_parse
import sys

# import config
# API_TOKEN = config.token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create private Bot API server endpoints wrapper
local_server = TelegramAPIServer.from_base(f'http://{sys.argv[1]}:8081')

# Initialize bot and dispatcher
bot = Bot(token=sys.argv[3], server=local_server)
dp = Dispatcher(bot)

IMAGE_REGEXP = r'http[s]?://.+'


@dp.message_handler(commands=['start'])
async def prov_playlists(message: types.Message):
    """
    Проверка плейлистов на новинки в них
    """
    await bot.set_my_commands(commands=[commands.commands, commands.commands2])
    url_s = db_sql.url_parse_db()
    url_s2 = [i[0] for i in url_s]

    await message.answer(f"<i>Подожди, {message.from_user.first_name} ... работаю</i>",
                         parse_mode=types.ParseMode.HTML)

    yotube_parse.main(url_s2)
    new_for_down = len(db_sql.for_down_db())  # количество возможных треков для загрузки
    await message.answer(text=f"<i>Приятного прослушивания,  {message.from_user.first_name}\n"
                              f"Новинок - {new_for_down}</i>",
                         parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=['send'])
async def send_in_chat(message: types.Message):
    """
    Загрузка и отправка аудиофайла в чат
    :param message:
    """
    new_down = len(db_sql.for_down_db())  # количество треков, которые будут загружены

    await message.answer(f"<i>Подожди, {message.from_user.first_name} ... работаю</i>",
                         parse_mode=types.ParseMode.HTML)

    for down in db_sql.for_down_db():
        yotube_parse.download_you(down[1])
        print('Отправка...')
        try:
            if get_os():
                path_title = f"{yotube_parse.get_directory()[0]}\\{down[2]}.m4a"  # путь до файла
            else:
                path_title = f"{yotube_parse.get_directory()[0]}/{down[2]}.m4a"  # путь до файла
            await bot.send_photo(chat_id=sys.argv[2], photo=InputFile.from_url(down[0]),
                                 caption=f'{down[1]}')

            await bot.send_audio(chat_id=sys.argv[2], audio=InputFile(path_title))
            os.remove(path_title)
            db_sql.upd_to_db(down[2])

        except:
            continue
    await message.answer(text=f"<i>Приятного прослушивания, {message.from_user.first_name}\n"
                              f"Новинок - {new_down}</i>",
                         parse_mode=types.ParseMode.HTML)


@dp.message_handler(content_types=['photo', 'sticker', 'document'])
async def get_doc_id(message: types.Message):
    await message.answer('<i> Прошу прощения.\nЯ не знаю такой команды.</i>',
                         parse_mode=types.ParseMode.HTML)


@dp.message_handler(filters.Regexp(IMAGE_REGEXP))
async def get_url_list(message: types.Message):
    """
    Получение и обработка URL от пользователя
    :param message: URL в текстовом формате
    """
    await bot.set_my_commands(commands=[commands.commands, commands.commands2])
    await message.answer(f"<i>Подожди, {message.from_user.first_name} ... работаю</i>",
                         parse_mode=types.ParseMode.HTML)
    db_sql.create_db2()
    yotube_parse.main(f'{message.text}')
    db_sql.insert_to_db2(f'{message.text}')
    new_for_down = len(db_sql.for_down_db())  # количество возможных треков для загрузки
    await message.answer(text=f"<i>Приятного прослушивания,  {message.from_user.first_name}\n"
                              f"Новинок - {new_for_down}</i>",
                         parse_mode=types.ParseMode.HTML)


@dp.message_handler()
async def zero_answer(message: types.Message):
    await bot.set_my_commands(commands=[commands.commands, commands.commands2])
    await message.answer('<i> Прошу прощения.\nЯ не знаю такой команды.</i>',
                         parse_mode=types.ParseMode.HTML)


def get_os():
    """
    Определяем версию операционной системы для дальнейшей корректировки путей
    """
    if os.name == 'nt':
        return True


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
