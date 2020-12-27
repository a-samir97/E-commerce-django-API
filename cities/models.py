from django.db import models

'''
[ 
    'Riyadh',
'Jeddah',
'Dammam',
'Al-Khobar',
'Dhahran',
'Al-Ahsa',
'Qatif',
'Jubail',
'Taif',
'Tabouk',
'Abha',
'Al Baha',
'Jizan',
'Najran',
'Makkah AL-Mukkaramah',
'AL-Madinah Al-Munawarah',
'Al Qaseem',
'Al-Jawf',
'Yanbu'
]

[
   ' مدينة الرياض',
'جدة',
'الدمام',
'الخبر',
'الظهران',
'الأحساء',
'القطيف',
'الجبيل',
'الطائف',
'تبوك',
'أبها',
'الباحة',
'جيزان',
'نجران',
'مكة المكرمة',
'المدينة المنورة',
'القصيم',
'الجوف',
'ينبع',
]
'''

class City(models.Model):
    name_en = models.CharField(max_length=30)
    name_ar = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.name_en  + ' | ' + self.name_ar