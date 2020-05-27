from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('listings/', include('listings.urls')),
    path('realtors/', include('realtors.urls')),
    path('admin/', admin.site.urls),
]
