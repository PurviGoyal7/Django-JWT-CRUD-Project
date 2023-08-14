from django.db import models

from users.models import Users


# Create your models here.
class Data(models.Model):
    data_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    
    def _str_(self):
        return '{} {} {}'.format(self.email, self.key, self.value)
    
