from django.contrib import admin
from .models import Problem, Category, UserSolvedProblems
from django.contrib.auth import get_user_model
# Register your models here.

admin.site.register(Problem)
admin.site.register(Category)
admin.site.register(UserSolvedProblems)
