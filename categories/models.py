from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    sub_categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name