from django.shortcuts import render
from .services import patient_service  # Passt den Import an euren genauen Pfad an

def home_view(request):
    return render(request, 'patient/home.html')

def search_view(request):
    query = request.GET.get('q', '').strip()
    
    patienten = []
    total_count = 0
    searched = False

    #TODO: Beispielcode muss in Realcode umgewandelt werden!
    # Wenn der User nach etwas gesucht hat (oder ihr standardmäßig alles listen wollt)
    if '' in request.GET:
        searched = True
        try:
            # Aufruf eures HTTP-Clients aus 'patient_service.py'
            api_response = patient_service.get_all(nachname=query, page=0, size=20)
            
            # Je nachdem, wie das FastAPI JSON strukturiert ist (z.B. {"items": [...], "total": 10})
            # Passen wir das hier an euer API-Response-Format an:
            patienten = api_response.get("items", [])
            total_count = api_response.get("total", len(patienten))
        except Exception as e:
            # Fehlerbehandlung, falls FastAPI offline ist
            print(f"API Error: {e}")
            total_count = 0

    context = {
        'query': query,
        'patienten': patienten,
        'total_count': total_count,
        'searched': searched,
    }
    
    return render(request, 'patient/search.html', context)