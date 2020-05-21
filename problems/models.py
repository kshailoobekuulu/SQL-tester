from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name
    

class Problem(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL,  related_name="problems")
    description = models.TextField()
    solution = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + ". " + self.description


class UserSolvedProblems(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="solved_problems")
    problem = models.ForeignKey(Problem, related_name='solved_problems', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "problem")

    def __str__(self):
        return self.user.username + " ------> " + str(self.problem.id)
