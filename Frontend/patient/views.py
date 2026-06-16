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

            total_rows = html_table.count("<tr")
            total_count = max(0, total_rows - 1) if total_rows > 0 else 0
            
        except Exception as e:
            print(f"🔎 FRONTEND ERROR: {type(e).__name__}: {e}")
            html_table = ""
            total_count = 0
            
        return render(request, "patient/search.html", {
            "query": query,
            "html_table": html_table,
            "total_count": total_count,
        })

    print("🔎 FRONTEND: Initialer Seitenaufruf")
    return render(request, "patient/search.html", {
        "query": "",
        "html_table": None,
        "total_count": 0,
    })