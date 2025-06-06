from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from quiz_utils import start_quiz, quiz_update, answer_update, ANSWERING
from settings import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


dp.message.register(start_quiz, commands=["start"])
dp.message.register(quiz_update, commands=["quiz"])
dp.callback_query.register(answer_update, state=ANSWERING)


async def main():
    await dp.start_polling(bot)

if __name__ == "main":
    import asyncio
    asyncio.run(main())
