# handlers/quiz.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler,
CallbackQueryHandler
from utils.quiz_utils import load_questions, get_random_question


WAITING, ANSWERING = range(2)


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать в викторину!\
                                     Нажми /quiz, чтобы начать.")
    return WAITING


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    questions = load_questions()
    if not questions:
        await update.message.reply_text("Вопросы не найдены!")
        return ConversationHandler.END

    question = get_random_question(questions)
    context.user_data["current_question"] = question
    context.user_data["score"] = context.user_data.get("score", 0)

    keyboard = [[InlineKeyboardButton(opt, callback_data=str(i)) for i, opt in
                enumerate(question["options"])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(question["question"],
                                    reply_markup=reply_markup)
    return ANSWERING


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_answer = int(query.data)
    question = context.user_data["current_question"]

    if user_answer == question["correct"]:
        context.user_data["score"] += 1
        await query.message.reply_text(f"Правильно!{question['explanation']}\n\
Твой счёт: {context.user_data['score']}\nНажми /quiz для следующего вопроса.")
    else:
        await query.message.reply_text(f"Неправильно!\
        {question['explanation']}\nНажми /quiz для следующего вопроса.")
    return WAITING


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Викторина окончена. Твой счёт:\
                                    {context.user_data.get('score', 0)}")
    return ConversationHandler.END

# Обработчик разговора
quiz_handler = ConversationHandler(
    entry_points=[CommandHandler("quiz", quiz)],
    states={
        WAITING: [CommandHandler("quiz", quiz)],
        ANSWERING: [CallbackQueryHandler(answer)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
