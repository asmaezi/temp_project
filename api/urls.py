from django.urls import path
from .views import receive_sensor_data, display_data

urlpatterns = [
    path('upload/', receive_sensor_data, name='upload_data'),
    path('dashboard/', display_data, name='dashboard'),
]