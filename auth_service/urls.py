
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Auth Service API",
        default_version="v1",
        description="API documentation for Auth Service",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def home(request):
    return HttpResponse("Hello from Adekunle,\n i'm more than just a junior dev, i'm always ready to learn and i'm a fast learning,\n You should to hire me ")

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.urls")),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

