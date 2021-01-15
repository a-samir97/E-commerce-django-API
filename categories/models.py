from django.db import models

class Category(models.Model):
    name_en = models.CharField(max_length=50)
    name_ar = models.CharField(max_length=50, null=True, blank=True)
    price = models.FloatField(default=10.0)
    uploaded_price = models.FloatField(default=10.0)
    msawm_team_price = models.FloatField(default=10.0)

    def __str__(self):
        return self.name_en

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='all_subcategories')
    name_en = models.CharField(max_length=50)
    name_ar = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name_en
    
    class Meta:
        verbose_name_plural = 'Subcategories'