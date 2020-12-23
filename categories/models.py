from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='all_subcategories', null=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name