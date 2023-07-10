from uuid import UUID
from django.http import Http404

from FCMManager import send_push
# from project.FCMManager import send_push
from .serializer import HouseSerializers,OperationSerializers
from rest_framework.response import Response
from rest_framework import status,generics,permissions
from .models import house,SalesOperations
from marketer.models import marketer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

class HouseCreate(generics.CreateAPIView):
        permission_classes = [permissions.IsAdminUser]
        serializer_class = HouseSerializers
        def post(self, request):
            try:
                serializers = HouseSerializers(data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return  Response(status= status.HTTP_200_OK, data=({
                        'status':status.HTTP_200_OK,
                        "data":serializers.data,
                        "message":"the house is added"
                    }))
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST,data=({'status':status.HTTP_400_BAD_REQUEST,
                                        "error":serializers.errors,
                                        }))
            except Exception as e:
                return Response(status= status.HTTP_500_INTERNAL_SERVER_ERROR,data =({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    "error": str(e),
                                    }))

class HouseList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = house.objects.all()
    serializer_class = HouseSerializers
    def list(self,request):
        houseData = self.get_queryset()
        serializer = HouseSerializers(houseData, many=True)
        
        data = serializer.data
        return Response(status= status.HTTP_200_OK ,data =({
            'status':status.HTTP_200_OK,
            "data":data}))
        
class HouseDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = house.objects.all()
    serializer_class = HouseSerializers
    lookup_field = "id"
    def page(self,request):
        queryset = self.get_queryset()
        serializer = HouseSerializers(queryset)
        return Response({'status':status.HTTP_200_OK,"data":serializer.data})

@api_view(['POST'])
def purchase_house(request):
    try:
        message = ''
        house_id = request.query_params.get('house_id', None)
        marketer_id = request.query_params.get('marketer_id', None)
        houseData = get_object_or_404(house, id=house_id)
        marketerData = get_object_or_404(marketer, id=marketer_id)
        print(houseData)
        if houseData.avaliableForSale == False:
            message = 'Sorry, this house not available for sale'
            return Response(status= status.HTTP_400_BAD_REQUEST, data= ({
                'status':status.HTTP_400_BAD_REQUEST,
                'message':message }))
            
        if marketerData.houseId.id == houseData.id:
            message = f'{houseData.name} Purchase successful'
            commission = houseData.price * marketerData.percentage
            marketerData.min_balance += commission
            houseData.avaliableForSale = False
            opearation =SalesOperations.objects.create(
                houseId = houseData,
                marketerId = marketerData,
                priceHouse = houseData.price,
                marketerCommission = commission,
            )
            serializer = OperationSerializers(opearation)
            marketerData.save()
            houseData.save()
            
            if marketerData.min_balance >= marketerData.min_amount:
                message = f'{houseData.name} Purchase successful , SEND AMOUNT'
                return Response(status= status.HTTP_200_OK, data=({
                    'status':status.HTTP_200_OK,
                    "data" : serializer.data,
                    'message': message }))
            return Response(status= status.HTTP_200_OK, data=({
                    'status':status.HTTP_200_OK,
                    "data" : serializer.data,
                    'message': message }))
        else:
            return Response(status= status.HTTP_400_BAD_REQUEST, data=({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message': 'this markter is not marketeing this house'
                    }))
    
    except Http404 as e:
        return Response(status= status.HTTP_400_BAD_REQUEST, data=({
                'status':status.HTTP_400_BAD_REQUEST,
                'message': str(e)
                }))
    except Exception as e:
        return Response(status= status.HTTP_500_INTERNAL_SERVER_ERROR, data=({
                'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e)
                }))


@api_view(['POST'])
def SendNotifcation(request):
    try:
        token = request.query_params.get('token', None)
        if not token:
            return Response({'error': 'Registration token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        send_push(request,token)
        return Response({'message': 'Push notification sent successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status= status.HTTP_500_INTERNAL_SERVER_ERROR, data=({
                'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e)
                }))
