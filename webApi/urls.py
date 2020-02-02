"""webApi URL Configuration

"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datapoints.views import DatapointList, DatapointSummaryList, DatapointUploadCsv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('rest_registration.api.urls')),
    path('datapoints/', csrf_exempt(DatapointList.as_view())),
    path('dataSummary/', DatapointSummaryList.as_view()),
    path('uploadCsvData/', DatapointUploadCsv.as_view()),
    path('favicon.ico',RedirectView.as_view(url='/static/favicon.ico')),
    path('', RedirectView.as_view(url='/static/index.html')),

]
