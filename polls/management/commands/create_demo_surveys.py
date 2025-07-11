# management/commands/create_demo_surveys.py
from django.core.management.base import BaseCommand
from polls.models import Survey, Question, Choice
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Creates demo surveys with different question types'

    def handle(self, *args, **options):
        # Очищаем старые данные
        Survey.objects.all().delete()

        # 1. Опрос по программированию
        programming = Survey.objects.create(
            title="Тест на знание Python",
            description="Проверьте свои знания языка программирования Python",
            end_date=timezone.now() + timezone.timedelta(days=30),
            is_active=True
        )

        # Вопрос 1 - одиночный выбор
        q1 = Question.objects.create(
            survey=programming,
            text="Какой оператор используется для возведения в степень в Python?",
            question_type=Question.SINGLE,
            order=1
        )
        Choice.objects.bulk_create([
            Choice(question=q1, text="**", is_correct=True),
            Choice(question=q1, text="^", is_correct=False),
            Choice(question=q1, text="pow()", is_correct=False),
            Choice(question=q1, text="//", is_correct=False)
        ])

        # Вопрос 2 - множественный выбор
        q2 = Question.objects.create(
            survey=programming,
            text="Какие из этих типов данных являются изменяемыми в Python?",
            question_type=Question.MULTIPLE,
            order=2
        )
        Choice.objects.bulk_create([
            Choice(question=q2, text="Список (list)", is_correct=True),
            Choice(question=q2, text="Кортеж (tuple)", is_correct=False),
            Choice(question=q2, text="Словарь (dict)", is_correct=True),
            Choice(question=q2, text="Множество (set)", is_correct=True)
        ])

        # Вопрос 3 - текстовый ответ
        q3 = Question.objects.create(
            survey=programming,
            text="Как называется функция для чтения ввода пользователя в Python 3?",
            question_type=Question.TEXT,
            correct_answer_text="input",
            order=3
        )

        # Вопрос 4 - одиночный выбор
        q4 = Question.objects.create(
            survey=programming,
            text="Какой декоратор используется для кэширования результатов функции?",
            question_type=Question.SINGLE,
            order=4
        )
        Choice.objects.bulk_create([
            Choice(question=q4, text="@lru_cache", is_correct=True),
            Choice(question=q4, text="@cache", is_correct=False),
            Choice(question=q4, text="@memoize", is_correct=False)
        ])

        # Вопрос 5 - множественный выбор
        q5 = Question.objects.create(
            survey=programming,
            text="Какие из этих модулей входят в стандартную библиотеку Python?",
            question_type=Question.MULTIPLE,
            order=5
        )
        Choice.objects.bulk_create([
            Choice(question=q5, text="json", is_correct=True),
            Choice(question=q5, text="requests", is_correct=False),
            Choice(question=q5, text="os", is_correct=True),
            Choice(question=q5, text="django", is_correct=False)
        ])

        # 2. Опрос по географии
        geography = Survey.objects.create(
            title="Тест на знание географии",
            description="Проверьте свои знания стран и столиц",
            end_date=timezone.now() + timezone.timedelta(days=15),
            is_active=True
        )

        # Вопрос 1 - одиночный выбор
        gq1 = Question.objects.create(
            survey=geography,
            text="Какая страна является самой большой по площади?",
            question_type=Question.SINGLE,
            order=1
        )
        Choice.objects.bulk_create([
            Choice(question=gq1, text="Россия", is_correct=True),
            Choice(question=gq1, text="Канада", is_correct=False),
            Choice(question=gq1, text="Китай", is_correct=False),
            Choice(question=gq1, text="США", is_correct=False)
        ])

        # Вопрос 2 - множественный выбор
        gq2 = Question.objects.create(
            survey=geography,
            text="Какие из этих стран находятся в Европе?",
            question_type=Question.MULTIPLE,
            order=2
        )
        Choice.objects.bulk_create([
            Choice(question=gq2, text="Франция", is_correct=True),
            Choice(question=gq2, text="Бразилия", is_correct=False),
            Choice(question=gq2, text="Италия", is_correct=True),
            Choice(question=gq2, text="Япония", is_correct=False)
        ])

        # Вопрос 3 - текстовый ответ
        gq3 = Question.objects.create(
            survey=geography,
            text="Как называется столица Австралии?",
            question_type=Question.TEXT,
            correct_answer_text="Канберра",
            order=3
        )

        # Вопрос 4 - одиночный выбор
        gq4 = Question.objects.create(
            survey=geography,
            text="Какое озеро является самым глубоким в мире?",
            question_type=Question.SINGLE,
            order=4
        )
        Choice.objects.bulk_create([
            Choice(question=gq4, text="Байкал", is_correct=True),
            Choice(question=gq4, text="Каспийское море", is_correct=False),
            Choice(question=gq4, text="Танганьика", is_correct=False),
            Choice(question=gq4, text="Верхнее", is_correct=False)
        ])

        # Вопрос 5 - множественный выбор
        gq5 = Question.objects.create(
            survey=geography,
            text="Какие из этих городов являются столицами?",
            question_type=Question.MULTIPLE,
            order=5
        )
        Choice.objects.bulk_create([
            Choice(question=gq5, text="Прага", is_correct=True),
            Choice(question=gq5, text="Санкт-Петербург", is_correct=False),
            Choice(question=gq5, text="Сидней", is_correct=False),
            Choice(question=gq5, text="Токио", is_correct=True)
        ])

        self.stdout.write(self.style.SUCCESS(
            'Создано 2 опроса с 10 вопросами (5 вопросов в каждом):\n'
            '1. Тест на знание Python\n'
            '2. Тест на знание географии'
        ))