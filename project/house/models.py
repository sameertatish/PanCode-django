from datetime import date
import uuid
from django.db import models

# from marketer.models import marketer

class house(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,null=False)
    image = models.ImageField(upload_to='image/',blank=True)
    description = models.CharField(max_length=100,null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    avaliableForSale = models.BooleanField(auto_created=True,default=True)
    createdDate = models.DateField(default=date.today)


    # def __str__(self):
    #     return self.name


    
class SalesOperations(models.Model):
    from marketer.models import marketer 
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    houseId = models.ForeignKey(house, related_name='purchased', on_delete=models.CASCADE)
    marketerId = models.ForeignKey(marketer, related_name='marketing', on_delete=models.CASCADE)
    priceHouse = models.DecimalField(max_digits=6, decimal_places=2)
    marketerCommission = models.DecimalField(max_digits=6, decimal_places=2)
    createdDate = models.DateField(default=date.today)
    
    # def __str__(self):
    #     return self.name