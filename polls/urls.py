from django.urls import path
from .views import HomeView, logout_view, CustomLoginView, RegisterView, SurveyDetailView, SurveyResultsView, \
    UserProfileView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('survey/<int:pk>/', SurveyDetailView.as_view(), name='survey_detail'),
    path('survey/<int:pk>/submit/', SurveyDetailView.as_view(), name='survey_submit'),
    path('survey/<int:pk>/results/', SurveyResultsView.as_view(), name='survey_results'),

]
