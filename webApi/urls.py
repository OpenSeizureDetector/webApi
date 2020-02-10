"""webApi URL Configuration

"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.routers import DefaultRouter
from datapoints.views import DatapointList, DatapointSummaryList, DatapointUploadCsv
from events.views import EventViewSet
from userdata.views import ProfileViewSet, LicenceViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'licence', LicenceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('rest_registration.api.urls')),
    path('datapoints/', csrf_exempt(DatapointList.as_view())),
    path('dataSummary/', DatapointSummaryList.as_view()),
    path('uploadCsvData/', DatapointUploadCsv.as_view()),
    #path('events/', EventViewSet.as_view()),
    path('', include(router.urls)),
    path('favicon.ico',RedirectView.as_view(url='/static/favicon.ico')),
    path('', RedirectView.as_view(url='/static/index.html')),

]
