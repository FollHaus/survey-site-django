from django.contrib import admin
from .models import Survey, Question, Choice, UserResponse


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    fields = ('text', 'is_correct', 'order')



@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Даты', {
            'fields': ('start_date', 'end_date'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('start_date',)
        return self.readonly_fields


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey', 'question_type', 'short_correct_answer')
    list_filter = ('survey', 'question_type')
    search_fields = ('text', 'correct_answer_text')
    inlines = [ChoiceInline]
    fieldsets = (
        (None, {
            'fields': ('survey', 'text', 'question_type')
        }),
        ('Правильный ответ (для текстовых вопросов)', {
            'fields': ('correct_answer_text',),
            'classes': ('collapse',)
        }),
    )

    def short_correct_answer(self, obj):
        if obj.question_type == Question.TEXT:
            return obj.correct_answer_text[:50] + '...' if obj.correct_answer_text else None
        return ", ".join([choice.text for choice in obj.choices.filter(is_correct=True)])

    short_correct_answer.short_description = 'Правильный ответ'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__survey')
    list_editable = ('is_correct',)
    search_fields = ('text',)
    ordering = ('question',)


@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey', 'question', 'answer_summary', 'created_at')
    list_filter = ('survey', 'question', 'user')
    search_fields = ('user__username', 'text_answer')
    readonly_fields = ('created_at',)

    def answer_summary(self, obj):
        if obj.question.question_type == Question.TEXT:
            return obj.text_answer
        return ", ".join([choice.text for choice in obj.selected_choices.all()])

    answer_summary.short_description = 'Ответ'