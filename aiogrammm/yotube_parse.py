#   Copyright (c) 2022. Сделано мной !!!

import os

import yt_dlp

import db_sql

from yt_dlp import YoutubeDL


def get_directory():
    """
    Формироавание пути к директории-хранилищу айдиофайлов
    :return:
    """
    if os.name == 'nt':  # for Windows
        musik_dir = f'C:\\{os.environ["HOMEPATH"]}\\Music'
        path1 = f'{musik_dir}\\%(id)s.%(ext)s'
        return [musik_dir, path1]
    else:  # for Posix
        musik_dir = f'/{os.environ["PWD"]}'
        path1 = f'{musik_dir}/%(id)s.%(ext)s'
        return [musik_dir, path1]


def download_you(webpage_url):
    """
    Загрузка аудио из URL файла
    :param webpage_url:
    """
    ydl_opts = {
        'ignoreerrors': 'True',
        'outtmpl': f'{get_directory()[-1]}',
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '320',
        }],
        'yes-playlist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        ydl.download([f'{webpage_url}'])


def parse_you(url):
    """
    Парсинг URL, создание и/или обновление базы аудиотреков
    :param url: URL для парсинга
    """
    ydl = YoutubeDL({'ignoreerrors': 'True'})
    info = ydl.extract_info(url, download=False)
    db_sql.create_db()
    if info.get('entries'):
        for key in info['entries']:
            try:
                if db_sql.select_in_db(key['id']):
                    continue
                else:
                    db_sql.insert_to_db(key['thumbnail'], key['webpage_url'], key['id'])
            except:
                continue
    else:
        try:
            if db_sql.select_in_db(info['id']):
                return
            else:
                db_sql.insert_to_db(info['thumbnail'], info['webpage_url'], info['id'])
        except:
            return


def main(u_rl='https://www.youtube.com/playlist?list=PLdE7uo_7KBkf1G8Ip9aFeyJJjglrZBM94'):
    """
    Задание исходного URL для парсинга
    :param u_rl: URL для парсинга - опционально - для проверки работы скрипта
    """
    if type(u_rl) == list:
        for url in u_rl:
            parse_you(url)
    else:
        parse_you(u_rl)


if __name__ == '__main__':
    main()
