import re
import math
from django.shortcuts import render
from .services import patient_service

def home_view(request):
    return render(request, 'patient/home.html')

def search_view(request):
    id_val = request.GET.get('id', '').strip()
    nachname_val = request.GET.get('nachname', '').strip()
    query_val = request.GET.get('query', '').strip()

    # Einheitlichen Suchbegriff ermitteln, je nachdem welches Feld gefüllt ist
    query = id_val or nachname_val or query_val

    # Prüfen, ob überhaupt ein Such-Event stattgefunden hat (Parameter in request.GET)
    if not any(k in request.GET for k in ['id', 'nachname', 'query']):
        print("🔎 FRONTEND: Initialer Seitenaufruf")
        return render(request, "patient/search.html", {
            "query": "",
            "id_val": "",
            "nachname_val": "",
            "html_table": None,
            "total_count": 0,
            "current_page": 0,
            "has_next": False,
            "filter_type": "Kein Filter"
        })

    print(f"🔎 FRONTEND: Suche nach Input: '{query}'")
    
    # Default-Variablen für das Template initialisieren
    html_table = ""
    total_elements = 0
    current_page = 0
    has_next = False
    
    # Keine Eingabe (Leere Gesamtsuche -> MIT SAUBERER PAGINATION)
    if not query:
        filter_type = "Kein Filter"
        try:
            page = max(0, int(request.GET.get('page', 0)))
        except (ValueError, TypeError):
            page = 0

        try:
            size = 10
            total_elements = patient_service.get_count()
            
            total_pages = math.ceil(total_elements / size) if total_elements > 0 else 1
            if page >= total_pages: 
                page = max(0, total_pages - 1)

            # Holt exakt die HTML-Tabelle für die aktuelle 10er-Seite
            html_table = patient_service.get_all_html(page=page, size=size)
            has_next = (page + 1) < total_pages
            current_page = page
        except Exception as e:
            print(f"GET_ALL API ERROR: {e}")

        return render(request, "patient/search.html", {
            "query": query, "id_val": id_val, "nachname_val": nachname_val,
            "html_table": html_table,
            "total_count": total_elements,
            "current_page": current_page,
            "prev_page": current_page - 1,
            "next_page": current_page + 1,
            "has_next": has_next,
            "filter_type": filter_type,
        })

    # VALIDIERUNG: Sonderzeichen abfangen
    if not re.match(r'^[a-zA-ZäöüÄÖÜß0-9\s\-]+$', query):
        return render(request, "patient/search.html", {
            "query": query,
            "id_val": id_val,
            "nachname_val": nachname_val,
            "html_table": "",
            "total_count": 0,
            "has_next": False,
            "filter_type": "Ungültig",
            "error_type": "validation_error",
            "error_message": "Ungültige Zeichen verwendet. Bitte nur Buchstaben oder Zahlen eingeben."
        })

    # ID (Reine Ziffern -> OHNE PAGINATION)
    if query.isdigit():
        filter_type = "ID"
        if not (1 <= len(query) <= 4):
            return render(request, "patient/search.html", {
                "query": query,
                "id_val": id_val,
                "nachname_val": nachname_val, 
                "html_table": "",
                "total_count": 0,
                "has_next": False,
                "filter_type": "Ungültig",
                "error_type": "validation_error",
                "error_message": "Die ID muss zwischen 1 und 4 Ziffern lang sein."
            })
        
        try:
            backend_html = patient_service.get_by_id_html(int(query))
            if backend_html:
                # Da das Backend bei der ID-Suche standardmäßig einen <article> liefert,
                # parsen wir die Werte per Regex, um sie in die gewohnte HTML-Tabelle einzubauen.
                p_id = re.search(r'<h2>Patient\s+(\d+)</h2>', backend_html, re.IGNORECASE)
                p_nachname = re.search(r'<strong>Nachname:</strong>\s*([^<]+)', backend_html, re.IGNORECASE)
                p_email = re.search(r'<strong>E-Mail:</strong>\s*([^<]+)', backend_html, re.IGNORECASE)
                p_geburtsdatum = re.search(r'<strong>Geburtsdatum:</strong>\s*([^<]+)', backend_html, re.IGNORECASE)
                p_geschlecht = re.search(r'<strong>Geschlecht:</strong>\s*([^<]+)', backend_html, re.IGNORECASE)
                p_familienstand = re.search(r'<strong>Familienstand:</strong>\s*([^<]+)', backend_html, re.IGNORECASE)
                p_adresse = re.search(r'<strong>Adresse:</strong>\s*([^<]+)', backend_html, re.IGNORECASE)
                
                plz, ort = "", ""
                if p_adresse:
                    adresse_parts = p_adresse.group(1).strip().split(" ", 1)
                    plz, ort = (adresse_parts[0], adresse_parts[1]) if len(adresse_parts) == 2 else (p_adresse.group(1).strip(), "")

                total_elements = 1
                html_table = f"""
                <table>
                    <thead>
                        <tr>
                            <th>ID</th><th>Nachname</th><th>E-Mail</th><th>Geburtsdatum</th>
                            <th>Geschlecht</th><th>Familienstand</th><th>PLZ</th><th>Ort</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{p_id.group(1).strip() if p_id else query}</td>
                            <td>{p_nachname.group(1).strip() if p_nachname else ''}</td>
                            <td>{p_email.group(1).strip() if p_email else ''}</td>
                            <td>{p_geburtsdatum.group(1).strip() if p_geburtsdatum else ''}</td>
                            <td>{p_geschlecht.group(1).strip() if p_geschlecht else ''}</td>
                            <td>{p_familienstand.group(1).strip() if p_familienstand else ''}</td>
                            <td>{plz}</td><td>{ort}</td>
                        </tr>
                    </tbody>
                </table>
                """
        except Exception as e:
            print(f"ID API ERROR: {e}")

    # Nachname (Buchstaben -> OHNE PAGINATION)
    else:
        filter_type = "Nachname"
        try:
            page = max(0, int(request.GET.get('page', 0)))
        except (ValueError, TypeError):
            page = 0

        try:
            size = 10

            total_elements = patient_service.get_count(nachname=query) 

            total_pages = (total_elements + size - 1) // size if total_elements > 0 else 1
            if page >= total_pages: 
                page = max(0, total_pages - 1)

            html_table = patient_service.get_all_html(nachname=query, page=page, size=size)
            
            has_next = (page + 1) < total_pages
            current_page = page
            
        except Exception as e:
            print(f"SUCHE API ERROR: {e}")

    return render(request, "patient/search.html", {
        "query": query, "id_val": id_val, "nachname_val": nachname_val,
        "html_table": html_table,
        "total_count": total_elements,
        "current_page": current_page,
        "prev_page": current_page - 1,
        "next_page": current_page + 1,
        "has_next": has_next,
        "filter_type": filter_type,
        "error_message": "",
    })