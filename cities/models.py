from django.db import models

'''
[ 'Riyadh', 'Jeddah', 'Mecca', 'Medina', 'Ad Dammām'
    'Al Hufūf', 'Buraydah', 'Al Ḩillah', 'Aţ Ţā’if', 'Tabūk'
    'Khamīs Mushayţ', 'Ḩā’il', 'Al Qaţīf', 'Al Mubarraz', 'Al Kharj'
    'Najrān','Abhā', '‘Ar‘ar', 'Sakākā', 'Jāzān', 'Al Bāḩah' ]
'''

class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name