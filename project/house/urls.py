from django.urls import path
from .views import HouseCreate,HouseList,HouseDetails,purchase_house,SendNotifcation

urlpatterns = [
    path('add/',HouseCreate.as_view()),
    path('get_all/',HouseList.as_view()),
    path('get='+'<str:id>/',HouseDetails.as_view()),
    path('purchase', purchase_house),
    path('sendNotfication', SendNotifcation)
]
