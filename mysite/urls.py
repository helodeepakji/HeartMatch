from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('app.urls')),
    path("chat/", include("chat.urls")),
    path("videocall/", include("videocall.urls")),
    path("admin/", admin.site.urls),
]