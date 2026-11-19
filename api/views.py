import json
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.dateparse import parse_date, parse_datetime
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData


def display_data(request):
    latest = SensorData.objects.order_by('-created_at').first()
    context = {
        'latest': latest,
    }
    return render(request, 'dashboard.html', context)


@csrf_exempt
def receive_sensor_data(request):
    if request.method == 'POST':
        try:
            if request.content_type and 'application/json' in request.content_type:
                payload = json.loads(request.body.decode('utf-8'))
            else:
                payload = request.POST

            temperature = payload.get('temperature')
            humidity = payload.get('humidity')

            if temperature is None or humidity is None:
                return JsonResponse(
                    {'error': 'temperature et humidity sont requis'},
                    status=400,
                )

            SensorData.objects.create(
                temperature=float(temperature),
                humidity=float(humidity),
            )
            return JsonResponse({'status': 'ok'}, status=201)
        except Exception as exc:
            return JsonResponse({'error': str(exc)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_chart_data(request):
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')

    queryset = SensorData.objects.all().order_by('created_at')

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

    if not start_str and not end_str:
        queryset = list(queryset)[-50:]
    else:
        queryset = list(queryset)

    return JsonResponse({
        'labels': [obj.created_at.strftime('%d/%m %H:%M') for obj in queryset],
        'temperatures': [obj.temperature for obj in queryset],
        'humidities': [obj.humidity for obj in queryset],
    })