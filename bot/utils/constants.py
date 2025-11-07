import html
import re

WELCOME_TEXT = (
    "👋 Привет! Я бот для подготовки к IT-собеседованиям.\n\n"
    "Ты можешь:\n"
    "🧠 Пройти тест по теме — например, *Python* или *SQL*\n"
    "🎯 Решить случайные вопросы\n"
    "📚 Изучить сборник вопросов — смотри ответы и объяснения\n"
    "🕐 Пройти экзамен — с ограничением по времени\n\n"
    "📊 Также доступно:\n"
    "🔁 Повторение ошибок — тренируй слабые места\n"
    "📈 Прогресс — отслеживай результаты и развитие\n"
    "🏆 Рейтинг — сравни себя с другими пользователями"
)

TEXT_MAIN_MENU = (
    "Вот что ты можешь делать в боте:\n\n"
    "🧠 Пройти тест по теме — например, *Python* или *SQL*\n"
    "🎯 Решить случайные вопросы\n"
    "📚 Изучить сборник вопросов — с ответами и объяснениями\n"
    "🕐 Пройти экзамен с ограничением по времени\n\n"
    "📊 Дополнительно:\n"
    "🔁 Повторять ошибки — тренируй слабые места\n"
    "📈 Отслеживать прогресс\n"
    "🏆 Смотреть рейтинг и сравнивать себя с другими пользователями"
)

TEST_TEXT = (
    "🧠 <b>Раздел: Тесты</b>\n\n"
    "Выберите тему, по которой хотите пройти тест:"
)
RQ_TEXT = (
        "🎲 <b>Раздел: Случайный вопрос</b>\n\n"
        "📘 Тренируйся отвечать на вопросы из базы знаний.\n"
        "Каждый вопрос подбирается случайно.\n\n"
        
        "Выберите действие:"
    )

EXAM_TEXT = (
        "🕐 <b>Раздел: Экзамен</b>\n\n"
        "📘 Тренируйся отвечать на вопросы в формате собеседования.\n"
        "Экзамен состоит из 15 вопросов. Время не ограничено — думай спокойно.\n\n"
        
        "Выберите действие:"
    )

def test_topic(topic):
    return (
        f"✅ Вы выбрали тему: <b>{topic}</b>\n\n"
        "Выберите уровень сложности:"
    )


def summary_text(topic: str, level: str) -> str:
    return (
        f"✅ Тема: <b>{topic}</b>\n"
        f"⚡ Уровень: <b>{level.capitalize()}</b>\n\n"
        "Готовы начать? Или измените тему/уровень ниже 👇"
    )


def text_level(topic, level):
    return (
        f"✅ Тема: <b>{topic}</b>\n"
        f"⚡ Уровень: <b>{level.capitalize()}</b>\n\n"
        "Нажмите кнопку ниже, чтобы начать тест:"
    )


def escape_md(text: str) -> str:
    """
    Экранирует все спецсимволы для Telegram MarkdownV2.
    """
    if not text:
        return ""
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)


def escape_html(text: str) -> str:
    """Экранирует HTML-спецсимволы, чтобы Telegram не падал."""
    if not text:
        return ""
    return html.escape(text)


def format_test_result(correct_answers: int, total_questions: int) -> str:
    """
    Форматирует текст с результатами теста для Telegram (HTML).
    """
    incorrect_answers = total_questions - correct_answers
    return (
        f"🎉 <b>Тест завершён!</b>\n\n"
        f"✅ <b>Правильных ответов:</b> {correct_answers}\n"
        f"❌ <b>Неправильных ответов:</b> {incorrect_answers}\n\n"
        f"📊 <b>Результат:</b> {correct_answers}/{total_questions}"
    )


def format_test_result_detailed(results, correct_count: int, total: int) -> str:
    """
    Форматирует подробный отчёт о тесте с ошибками в Telegram (HTML-разметка).

    Args:
        results (list): Список результатов по вопросам.
        correct_count (int): Количество правильных ответов.
        total (int): Общее количество вопросов.

    Returns:
        str: Готовый HTML-текст для отправки пользователю.
    """

    text_lines = [
        f"📊 <b>Ваш результат:</b> {correct_count} из {total} ✅",
        "",
        "<b>Ошибки:</b>"
    ]

    separator = "━━━━━━━━━━━━━━━━━━"

    for i, r in enumerate(results, start=1):
        if r.is_correct:
            continue

        q = r.question
        question_text = escape_html(q.question_text)
        correct_option_text = escape_html(q.options[q.correct_option])
        explanation = escape_html(q.explanation or "Нет объяснения")

        text_lines.append(
            f"{separator}\n\n"
            f"❌ <b>№{i}.</b> {question_text}\n"
            f"✅ <b>{correct_option_text}</b>\n"
            f"💡 <i>{explanation}</i>\n"
        )

    return "\n".join(text_lines).strip()
