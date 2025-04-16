"""webApi URL Configuration

"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

from datapoints.views import DatapointViewSet, DatapointSummaryList, DatapointUploadCsv
from events.views import EventViewSet
from userdata.views import ProfileViewSet

router = DefaultRouter()
router.register(r'api/events', EventViewSet)
router.register(r'api/datapoints', DatapointViewSet)
#router.register(r'api/user', UserViewSet)
router.register(r'api/profile', ProfileViewSet)
#router.register(r'api/licence', LicenceViewSet)

urlpatterns = [
    #path('api/admin/', admin.site.urls),
    path('api/accounts/', include('rest_registration.api.urls')),
    #path('api/datapoints/', csrf_exempt(DatapointList.as_view())),
    path('api/dataSummary/', DatapointSummaryList.as_view()),
    path('api/uploadCsvData/', DatapointUploadCsv.as_view()),
    #path('events/', EventViewSet.as_view()),
    path('', include(router.urls)),
    path('favicon.ico',RedirectView.as_view(url='/static/favicon.ico')),
    path(r'', TemplateView.as_view(template_name='index.html')),
    #path('', RedirectView.as_view(url='/static/index.html')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
