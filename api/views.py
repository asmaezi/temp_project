import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.mail import send_mail
from .models import SensorData


@csrf_exempt
def receive_sensor_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            temp = data.get('temperature')
            hum = data.get('humidity')

            if temp is not None and hum is not None:
                temperature = float(temp)
                humidity = float(hum)

                # Enregistrer la mesure dans la base de données
                SensorData.objects.create(temperature=temperature, humidity=humidity)

                # VÉRIFICATION DE L'INTERVALLE (Ex: Alerte si < 20°C ou > 23°C)
                if temperature < 20.0 or temperature > 23.0:
                    sujet = "🚨 ALERTE LABO : Température anormale !"
                    message = (
                        f"Attention !\n\n"
                        f"La température actuelle est de {temperature} °C, "
                        f"ce qui dépasse l'intervalle sécurisé (20°C - 23°C).\n"
                        f"Veuillez intervenir d'urgence !"
                    )
                    destinataire = ['asmaezinerotaracteheio@gmail.com']  # Ton email

                    try:
                        send_mail(sujet, message, None, destinataire, fail_silently=False)
                    except Exception as mail_err:
                        print(f"Erreur d'envoi d'email : {mail_err}")

                return JsonResponse({'status': 'success', 'message': 'Données enregistrées !'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Champs manquants'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)


def display_data(request):
    records = SensorData.objects.all().order_by('-created_at')
    latest = records.first()

    # Calculer le nombre d'alertes (température hors normes)
    alert_count = sum(1 for r in records if r.temperature < 20.0 or r.temperature > 23.0)

    # Déterminer le statut des incidents pour le bloc du milieu
    if latest:
        if 20.0 <= latest.temperature <= 23.0:
            incident_status = "Pas d'incident"
            status_color = "text-success"
        else:
            incident_status = "ALERTE : Seuil dépassé !"
            status_color = "text-danger"
    else:
        incident_status = "Aucune donnée"
        status_color = "text-muted"

    records_sorted = list(reversed(records[:20]))
    labels = [r.created_at.strftime('%H:%M:%S') for r in records_sorted]
    temperatures = [float(r.temperature) for r in records_sorted]
    humidities = [float(r.humidity) for r in records_sorted]

    context = {
        'records': records[:20],
        'latest': latest,
        'alert_count': alert_count,
        'incident_status': incident_status,
        'status_color': status_color,
        'labels': labels,
        'temperatures': temperatures,
        'humidities': humidities,
    }
    return render(request, 'api/dashboard.html', context)