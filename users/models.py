from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=False)
    password = models.CharField(max_length=50, null=False)
    full_name = models.CharField(max_length=50, null=False)
    age = models.PositiveIntegerField(null=False)
    gender = models.CharField(max_length=12)
    
    def _str_(self):
        return '{} {}'.format(self.username, self.email)
    
    
