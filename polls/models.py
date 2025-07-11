from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def get_correct_answers_count(self, user):
        """Количество правильных ответов конкретного пользователя"""
        return self.responses.filter(user=user, is_correct=True).count()

    @property
    def total_questions_count(self):
        """Общее количество вопросов в опросе"""
        return self.questions.count()

    def get_last_response_date(self, user):
        """Дата последнего ответа пользователя"""
        try:
            return self.responses.filter(user=user).latest('created_at').created_at
        except UserResponse.DoesNotExist:
            return None


class Question(models.Model):
    TEXT = 'text'
    SINGLE = 'single'
    MULTIPLE = 'multiple'

    QUESTION_TYPE_CHOICES = [
        (TEXT, 'Текстовый ответ'),
        (SINGLE, 'Один вариант'),
        (MULTIPLE, 'Несколько вариантов'),
    ]

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES)
    correct_answer_text = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)



class UserResponse(models.Model):
    user = models.ForeignKey(User, related_name='responses', on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='responses', on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)
    selected_choices = models.ManyToManyField(Choice, related_name='user_responses')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_correct(self):
        """Проверяет правильность ответа"""
        if self.question.question_type == Question.TEXT:
            return (self.text_answer or '').lower() == (self.question.correct_answer_text or '').lower()

        elif self.question.question_type == Question.SINGLE:
            selected = self.selected_choices.first()
            return selected and selected.is_correct

        elif self.question.question_type == Question.MULTIPLE:
            correct_choices = set(self.question.choices.filter(is_correct=True).values_list('id', flat=True))
            selected_ids = set(self.selected_choices.values_list('id', flat=True))
            return correct_choices == selected_ids

        return False