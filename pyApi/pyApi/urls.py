"""pyApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
import wearers.views
import rawdata.views

router = routers.DefaultRouter()
router.register(r'users', wearers.views.UserViewSet)
router.register(r'groups', wearers.views.GroupViewSet)
router.register(r'wearers', wearers.views.WearerViewSet)
router.register(r'licence', wearers.views.LicenceViewSet)
#router.register(r'datapoints', rawdata.views.DatapointViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include('rawdata.urls')),
]
