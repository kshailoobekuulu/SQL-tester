from django.urls import path
from .views import test_view, problems_list_view

urlpatterns = [
    path('', problems_list_view, name='problem_list'),
    path('<int:pk>/', test_view, name='test'),
]

