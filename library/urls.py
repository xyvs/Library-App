from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('master/', admin.site.urls),
	path('accounts/', include('django.contrib.auth.urls')),
	path('', include('index.urls')),
	path('api/', include('api.urls'))
]
