from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ESTO ES LO IMPORTANTE
    path('', include('checklist.urls')),
]
