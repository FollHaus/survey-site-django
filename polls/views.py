from django.db.models import Count, Max
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import DetailView
from .models import Survey

from django.db.models import Count
from django.views.generic import DetailView
from django.db.models import Prefetch
from .models import Survey, Question, Choice, UserResponse


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'polls/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Регистрация прошла успешно! Теперь вы можете войти.'
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Пожалуйста, исправьте ошибки в форме.'
        )
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = 'polls/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Неверные учетные данные')
        return super().form_invalid(form)


class HomeView(View):
    template_name = 'polls/home.html'

    def get(self, request):
        if request.user.is_authenticated:
            active_surveys = Survey.objects.filter(is_active=True)
            return render(request, self.template_name, {'active_surveys': active_surveys})

        login_form = AuthenticationForm()
        register_form = UserCreationForm()
        return render(request, self.template_name, {
            'login_form': login_form,
            'register_form': register_form
        })

    def post(self, request):
        if 'login' in request.POST:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Добро пожаловать, {username}!")
                    return redirect('home')
            messages.error(request, "Неверное имя пользователя или пароль")
            return render(request, self.template_name, {
                'login_form': form,
                'register_form': UserCreationForm()
            })

        elif 'register' in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Регистрация прошла успешно!")
                return redirect('home')
            return render(request, self.template_name, {
                'login_form': AuthenticationForm(),
                'register_form': form
            })

        return redirect('home')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из системы")
    return redirect('login')


# views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'polls/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Получаем все анкеты с аннотацией последней даты ответа
        surveys = Survey.objects.filter(
            responses__user=user
        ).annotate(
            last_response_date=Max('responses__created_at')
        ).order_by('-last_response_date')

        # Добавляем статистику для каждого опроса
        surveys_with_stats = []
        for survey in surveys:
            # Получаем все ответы пользователя на этот опрос
            responses = survey.responses.filter(user=user).prefetch_related(
                'selected_choices', 'question'
            )

            # Считаем правильные ответы
            correct_answers = sum(1 for r in responses if r.is_correct())
            total_questions = survey.questions.count()

            surveys_with_stats.append({
                'survey': survey,
                'last_response_date': survey.last_response_date,
                'correct_answers': correct_answers,
                'total_questions': total_questions
            })

        context['surveys_with_stats'] = surveys_with_stats
        return context


class SurveyDetailView(DetailView):
    model = Survey
    template_name = 'polls/survey_detail.html'
    context_object_name = 'survey'

    def get_queryset(self):
        return Survey.objects.prefetch_related('questions__choices').filter(is_active=True)

    def post(self, request, *args, **kwargs):
        survey = self.get_object()
        user = request.user
        # Удаляем старые ответы пользователя на этот опрос
        UserResponse.objects.filter(user=request.user, survey=survey).delete()

        for question in survey.questions.all():
            response_key = f'question_{question.id}'

            if question.question_type == Question.TEXT:
                answer_text = request.POST.get(response_key)
                if answer_text:
                    UserResponse.objects.create(
                        user=user,
                        survey=survey,
                        question=question,
                        text_answer=answer_text
                    )

            elif question.question_type == Question.SINGLE:  # Было SINGLE_CHOICE
                choice_id = request.POST.get(response_key)
                if choice_id:
                    choice = question.choices.get(id=choice_id)
                    UserResponse.objects.create(
                        user=user,
                        survey=survey,
                        question=question,
                    ).selected_choices.add(choice)

            elif question.question_type == Question.MULTIPLE:  # Было MULTIPLE_CHOICE
                choice_ids = request.POST.getlist(response_key)
                if choice_ids:
                    response = UserResponse.objects.create(
                        user=user,
                        survey=survey,
                        question=question,
                    )
                    for choice_id in choice_ids:
                        choice = question.choices.get(id=choice_id)
                        response.selected_choices.add(choice)

        messages.success(request, 'Спасибо! Ваши ответы сохранены.')
        return redirect('survey_results', pk=survey.pk)


class SurveyResultsView(DetailView):
    model = Survey
    template_name = 'polls/survey_results.html'

    def get_queryset(self):
        return Survey.objects.prefetch_related(
            Prefetch(
                'questions__choices',
                queryset=Choice.objects.annotate(
                    response_count=Count('user_responses')
                )
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.object
        user = self.request.user

        total_questions = survey.questions.count()

        # Уникальные участники
        participant_ids = UserResponse.objects.filter(
            survey=survey
        ).values_list('user', flat=True).distinct()
        total_participants = participant_ids.count()

        # Ответы пользователя: сгруппированы по вопросам
        user_responses = UserResponse.objects.filter(
            survey=survey,
            user=user
        ).select_related('question').prefetch_related('selected_choices')

        # Группировка по вопросам: {question_id: [responses]}
        from collections import defaultdict
        grouped_by_question = defaultdict(list)
        for resp in user_responses:
            grouped_by_question[resp.question_id].append(resp)

        # Правильные ответы: по одному на каждый вопрос
        user_correct = 0
        for responses in grouped_by_question.values():
            if any(r.is_correct() for r in responses):
                user_correct += 1

        user_average_score = f"{user_correct}/{total_questions}"

        # Средний результат по всем участникам
        participant_scores = []
        for pid in participant_ids:
            responses = UserResponse.objects.filter(
                survey=survey,
                user_id=pid
            ).select_related('question').prefetch_related('selected_choices')

            grouped = defaultdict(list)
            for r in responses:
                grouped[r.question_id].append(r)

            correct = 0
            for group in grouped.values():
                if any(r.is_correct() for r in group):
                    correct += 1

            participant_scores.append(correct / total_questions)

        avg_score = (sum(participant_scores) / len(participant_scores)) if participant_scores else 0

        # Формируем данные по вопросам
        questions_data = []
        for question in survey.questions.prefetch_related(
                Prefetch('choices', queryset=Choice.objects.annotate(response_count=Count('user_responses')))
        ):
            user_resp_group = grouped_by_question.get(question.id, [])
            user_resp = user_resp_group[0] if user_resp_group else None  # Один из ответов (для отображения)

            total_responses = question.responses.count()
            choices = []
            for choice in question.choices.all():
                rc = choice.response_count
                perc = round((rc / total_responses * 100) if total_responses else 0, 1)
                selected = any(resp.selected_choices.filter(id=choice.id).exists() for resp in user_resp_group)
                choices.append({
                    'id': choice.id,
                    'text': choice.text,
                    'is_correct': choice.is_correct,
                    'response_count': rc,
                    'response_percentage': perc,
                    'user_selected': selected
                })

            questions_data.append({
                'id': question.id,
                'text': question.text,
                'question_type': question.question_type,
                'correct_answer_text': question.correct_answer_text,
                'user_answer': {
                    'text_answer': user_resp.text_answer if user_resp else None,
                    'is_correct': any(r.is_correct() for r in user_resp_group) if user_resp_group else False,
                    'selected_choice_ids': list(
                        user_resp.selected_choices.values_list('id', flat=True)) if user_resp else []
                },
                'choices': choices,
                'chart_type': 'bar' if question.question_type == Question.SINGLE else 'pie'
            })

        context.update({
            'total_questions': total_questions,
            'total_participants': total_participants,
            'user_score': user_average_score,
            'user_correct_answers': user_correct,
            'avg_correct_answers': round(avg_score * total_questions, 1),
            'questions_with_stats': questions_data
        })
        return context
