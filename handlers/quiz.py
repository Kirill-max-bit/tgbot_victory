from aiogram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ContextTypes, ConversationHandler, Command
from aiogram.handlers import CallbackQueryHandler
from quiz_utils import load_questions, get_random_question

ANSWERING = 0


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Добро пожаловать в викторину! "
                                    "Нажми /quiz, чтобы начать")
    return ConversationHandler.END


async def quiz_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    questions = load_questions()
    if not questions:
        await update.message.reply_text("Вопросы не найдены!")
        return ConversationHandler.END

    question = get_random_question(questions)
    context.user_data["current_question"] = question
    context.user_data["score"] = context.user_data.get("score", 0)

    keyboard = [
        [
            InlineKeyboardButton(
                opt,
                callback_data=str(i)
            ) for i, opt in enumerate(question["options"])
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        question["question"],
        reply_markup=reply_markup
    )
    return ANSWERING


async def answer_update(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()

    user_answer = int(query.data)
    question = context.user_data["current_question"]
    explanation = question.get("explanation", "Пояснение отсутствует.")

    if user_answer == question["correct"]:
        context.user_data["score"] += 1

    await query.edit_message_text(
        f"Ваш ответ: {user_answer}\n"
        f"Правильный ответ: {question['correct']}\n"
        f"{explanation}"
    )
    return ConversationHandler.END
