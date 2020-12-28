from django.db import models

class Category(models.Model):
    name_en = models.CharField(max_length=50)
    name_ar = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name_en


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='all_subcategories')
    name_en = models.CharField(max_length=50)
    name_ar = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name_en