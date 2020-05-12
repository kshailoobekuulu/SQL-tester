from django.db import models

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
        return self.description
    
