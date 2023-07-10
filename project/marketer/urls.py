from django.urls import path
from .views import MarketerView,MarketerList,MarketerDetails

urlpatterns = [
    path('add/',MarketerView.as_view()),
    path('get_all/',MarketerList.as_view()),
    path('get='+'<str:id>/',MarketerDetails.as_view())
]
