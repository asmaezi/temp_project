from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/api/dashboard/')),  # <-- Redirige directement vers le dashboard
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    path('chart-data/', views.get_chart_data, name='chart_data'),
]