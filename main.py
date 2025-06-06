from aiogram import Application, CommandHandler
from config.settings import BOT_TOKEN
from handlers.start import start, help_command
from handlers.quiz import quiz_handler


async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(quiz_handler)
    await app.run_polling()

if __name__ == "main":
    import asyncio
    asyncio.run(main())
