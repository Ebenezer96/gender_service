from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

def home(request):
    return JsonResponse({
        "status": "success",
        "message": "Gender service is running"
    })

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]