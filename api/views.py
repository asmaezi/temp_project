from django.http import JsonResponse
from django.utils.dateparse import parse_datetime, parse_date
from .models import SensorData

def get_chart_data(request):
    start_str = request.GET.get('start')  # ex: "2026-11-19T08:00" ou "2026-11-19"
    end_str = request.GET.get('end')      # ex: "2026-11-19T18:00" ou "2026-11-19"

    queryset = SensorData.objects.all().order_by('created_at')  # Remplace 'created_at' par le nom exact de ton champ date

    if start_str:
        dt_start = parse_datetime(start_str)
        if dt_start:
            queryset = queryset.filter(created_at__gte=dt_start)
        elif parse_date(start_str):
            queryset = queryset.filter(created_at__date__gte=parse_date(start_str))

    if end_str:
        dt_end = parse_datetime(end_str)
        if dt_end:
            queryset = queryset.filter(created_at__lte=dt_end)
        elif parse_date(end_str):
            queryset = queryset.filter(created_at__date__lte=parse_date(end_str))

    # Si aucun filtre n'est choisi, on limite aux 50 dernières mesures pour garder le graphe lisible
    if not start_str and not end_str:
        queryset = list(queryset)[-50:]

    data = {
        'labels': [obj.created_at.strftime('%d/%m %H:%M') for obj in queryset],
        'temperatures': [obj.temperature for obj in queryset],
        'humidities': [obj.humidity for obj in queryset],
    }
    return JsonResponse(data)