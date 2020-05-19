from django.urls import path
from .views import test_view, problems_by_category_view, solved_problems_by_current_user_view

urlpatterns = [
    path('<str:category>/', problems_by_category_view, name='problems_by_category'),
    path('solved/', solved_problems_by_current_user_view, name='solved_problems'),
    path('submit/<int:pk>/', test_view, name='test'),
]
