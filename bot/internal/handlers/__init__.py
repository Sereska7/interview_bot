from bot.internal.handlers.start import router as router_start
from bot.internal.handlers.test import router as router_test
from bot.internal.handlers.exam import router as router_exam
from bot.internal.handlers.progress import router as router_progress
from bot.internal.handlers.question_book import router as router_question_book
from bot.internal.handlers.random_question import router as router_random_question
from bot.internal.handlers.subscription import router as router_subscription

routers = [
    router_start,
    router_test,
    router_exam,
    router_question_book,
    router_random_question,
    router_progress,
    router_subscription
]
