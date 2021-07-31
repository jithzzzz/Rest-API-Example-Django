from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from Payments import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('Payments.urls')),
]

