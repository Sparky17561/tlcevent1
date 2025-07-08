# tlcevent1/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # <— Add this line to include your app’s URLconf:
    path('', include('qrvalidator.urls')),  
]
