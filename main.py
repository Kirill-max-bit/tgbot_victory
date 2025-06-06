import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

logger.add(
    "logs/bot.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True
)


async def create_bot():
    token = os.getenv('TOKEN')
    if not token:
        logger.error("Токен бота не найден в переменных окружения!")
        raise ValueError("Токен бота не установлен")

    bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # другие папки, которые надо заменить
    logger.info("Бот и диспетчер успешно настроены")
    return bot, dp


async def main():
    bot = None
    try:
        bot, dp = await create_bot()

        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Очередь обновлений очищена")

        logger.info("Запуск бота...")
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )

    except asyncio.CancelledError:
        logger.info("Получен сигнал на завершение работы")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")

        if bot and bot.session:
            try:
                await bot.session.close()
                logger.info("Сессия бота успешно закрыта")
            except Exception as e:
                logger.error(f"Ошибка при закрытии сессии: {e}")

        logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен по запросу пользователя")
    except Exception as e:
        logger.critical(f"Необработанная ошибка: {e}")
