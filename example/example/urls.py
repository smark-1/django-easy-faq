from django.urls import path, include
from django.contrib import admin
from home.views import home

urlpatterns = [
    path("", home),
    path('faq/', include('faq.urls')),
    path("admin/", admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
]

