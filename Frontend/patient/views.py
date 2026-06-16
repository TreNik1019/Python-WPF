from django.shortcuts import render
from .services import patient_service


def home_view(request):
    return render(request, 'patient/home.html')


def search_view(request):
    if 'query' in request.GET:
        query = request.GET.get('query', '').strip()
        print(f"🔎 FRONTEND: Suche nach: '{query}'")
        
        try:
            print("🔎 FRONTEND: Calling backend")

            html_table = patient_service.get_all(
                nachname=query,
                page=0,
                size=20
            )
            print("🔎 FRONTEND: HTML received")
            
        except Exception as e:
            print(f"🔎 FRONTEND ERROR: {type(e).__name__}: {e}")
            html_table = ""
            
        return render(request, "patient/search.html", {
            "query": query,
            "html_table": html_table,
        })

    print("🔎 FRONTEND: Initialer Seitenaufruf")
    return render(request, "patient/search.html", {
        "query": "",
        "html_table": None,
    })