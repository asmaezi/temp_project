from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.display_data, name='dashboard'),
    path('upload/', views.receive_sensor_data, name='upload_data'),
    path('post/', views.receive_sensor_data, name='post_data'),
    path('chart-data/', views.get_chart_data, name='chart_data'),
]