from datetime import date
import uuid
from django.db import models
from house.models import house

class marketer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,null=False)
    houseId = models.ForeignKey(house, related_name='marketers', on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    createdDate = models.DateField(default=date.today)
    percentage = models.DecimalField(max_digits=7, decimal_places=2)
    min_balance = models.DecimalField(max_digits=7, decimal_places=2)
    reference_code = models.CharField(max_length=20)
    min_amount = models.DecimalField(max_digits=7, decimal_places=2,default=500) 
    
    # def __str__(self):
    #     return self.name

