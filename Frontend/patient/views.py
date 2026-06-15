from django.shortcuts import render
from .services import patient_service


def home_view(request):
    return render(request, 'patient/home.html')


def search_view(request):
    query = request.GET.get('q', '').strip()
    print(f"🔎 FRONTEND: Incoming query: '{query}'")

    html_table = ""

    try:
        print("🔎 FRONTEND: Calling backend")

        # 🔥 wenn query leer ist → einfach alle holen
        html_table = patient_service.get_all(
            nachname=query,   # leer string = keine Filterung
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