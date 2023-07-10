from  .models import marketer
from rest_framework import serializers
from house.models import house

class MarkterSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    reference_code = serializers.CharField(required=True, max_length=100)
    gender = serializers.ChoiceField( choices=[('M', 'Male'), ('F', 'Female')])
    percentage = serializers.FloatField(required=True)
    min_balance = serializers.FloatField(required=True)
    houseId = serializers.PrimaryKeyRelatedField(queryset=house.objects.all())
    min_amount = serializers.FloatField(required=True)
    createdDate = serializers.DateField(read_only = True)
    
    class Meta:
        model = marketer
        fields = '__all__'
        



    # def get_house(self, obj):
    #     house_obj = obj.house
    #     if house_obj:
    #         return {
    #             'id': str(house_obj.id),
    #             'name': house_obj.name,
    #             'image': house_obj.image.url if house_obj.image else None,
    #             'description': house_obj.description,
    #             'price': house_obj.price,
    #             'avaliableForSale' : house_obj.avaliableForSale
    #         }
    #     else:
    #         return None
  