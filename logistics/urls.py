"""realestate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings
from django.conf.urls.static import static
from .views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Logistics API",
        default_version="v1",
    ),
    public=True,
)

urlpatterns = [
    path('', redirect_swagger_view),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("api/", include("app_auth.urls")),
    path("api/", include("core.urls")),
    path("api/", include("info.urls")),
    path("api/", include("staff.urls")),
]

admin.site.site_header = "SGMyanmar Backend Administration"
admin.site.site_title = "SGMyanmar Backend Administration"
admin.site.index_title = "SGMyanmar Backend Administration"
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)