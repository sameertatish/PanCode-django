# from project.marketer.serializer import MarkterSerializers
from  .models import house,SalesOperations
from marketer.models import marketer
from marketer.serializer import MarkterSerializers
from rest_framework import serializers

class HouseSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    marketer = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(required=False,)
    description = serializers.CharField(required=True,max_length=60)
    price = serializers.FloatField()
    avaliableForSale = serializers.BooleanField(default=True)
    class Meta:
        model = house
        fields = '__all__'

    def get_marketer(self, obj):
        queryset = marketer.objects.select_related('houseId').filter(houseId=obj.id)
        if queryset.exists():
            serializers = MarkterSerializers(queryset, many=True)
            return serializers.data
        else:
            return []
        
class OperationSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalesOperations
        fields = '__all__'

