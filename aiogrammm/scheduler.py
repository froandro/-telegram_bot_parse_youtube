import asyncio
import aioschedule
import aio_bot


async def scheduler():
    """
    Установка расписания для запуска загрузки возможных аудиофайлов в чат
    """
    aioschedule.every().day.at("12:35").do(aio_bot.send_in_chat)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(x):
    """
    Задание на запуск расписания выполнения скрипта
    :param x:
    """
    asyncio.create_task(scheduler())


def main():
    aio_bot.executor.start_polling(aio_bot.dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
