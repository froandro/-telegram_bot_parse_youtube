import sqlite3 as sq


def drop_db():
    """
    Очистка базы данных от таблицы с данными URL файлов
    """
    with sq.connect('bot-db/yotube_parse.db') as con:
        cur = con.cursor()
        cur.execute("""DROP TABLE files""")
        con.commit()


def create_db():
    """
    Создание таблицы с данными URL файлов для загрузки
    """
    with sq.connect('bot-db/yotube_parse.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS files (
                        thumbnail TEXT,
                        webpage_url TEXT,
                        id TEXT,
                        download INTEGER DEFAULT 0
                         )""")
        con.commit()


def create_db2():
    """
    Создание таблицы с URL, полученных от пользователя через 'message' чата
    """
    with sq.connect('bot-db/yotube_parse.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS playlists (
                        webpage_url TEXT NOT NULL UNIQUE
                         )""")
        con.commit()


def insert_to_db2(*value_parse: str):
    """
    Вставка в таблицу URL, полученных от пользователя через 'message' чата
    :param value_parse: URL, полученные от пользователя через 'message' чата
    """
    try:
        with sq.connect('bot-db/yotube_parse.db') as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO playlists ('webpage_url') VALUES (?)""", value_parse)
            con.commit()
    except sq.IntegrityError:
        return


def insert_to_db(*value_parse: str):
    """
    Вставка в табдицу данных, полученных из парсинга URL
    :param value_parse: данные, полученных из парсинга
    """
    with sq.connect('bot-db/yotube_parse.db') as con:
        cur = con.cursor()
        cur.execute("""INSERT INTO files ('thumbnail', 'webpage_url', 'id') VALUES (?, ?, ?)""", value_parse)
        con.commit()


def upd_to_db(id_parse):
    """
    Обновление данных в таблице, после загрузки аудиофайла в чат
    :param id_parse: id загруженного файла
    """
    with sq.connect('bot-db/yotube_parse.db') as con:
        cur = con.cursor()
        t = (f'{id_parse}',)
        cur.execute("""UPDATE files SET download=1 WHERE id=?""", t)
        con.commit()


def select_in_db(id_parse):
    """
    Проверка наличия данных в базе
    :param id_parse: id файла в базе
    :return:
    """
    with sq.connect('bot-db/yotube_parse.db') as con:
        cur = con.cursor()
        t = (f'{id_parse}',)
        cur.execute(f"""SELECT thumbnail FROM files WHERE id=?""", t)
        return cur.fetchone()


def for_down_db():
    """
    Выборка треков для последующей загрузки
    """
    with sq.connect('bot-db/yotube_parse.db') as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM files WHERE download=0""")
        return cur.fetchall()


def url_parse_db():
    """
    Выборка URL плейлистов для последующей проверки на новинки в них
    """
    with sq.connect('bot-db/yotube_parse.db') as con:
        cur = con.cursor()
        cur.execute(f"""SELECT webpage_url FROM playlists""")
        return cur.fetchall()


if __name__ == '__main__':
    pass
