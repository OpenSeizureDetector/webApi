from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rawdata import views

urlpatterns = [
    path('datapoints/', views.DatapointList.as_view()),
    path('datapoints/<int:pk>/', views.DatapointDetail.as_view()),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
