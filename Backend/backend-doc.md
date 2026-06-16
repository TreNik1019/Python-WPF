# Backend

## Aufbau des Backends

Das Backend wurde mit Python und dem Webframework FastAPI entwickelt. Es stellt die Schnittstelle zwischen Frontend und den gespeicherten Patientendaten dar. Alle Suchanfragen des Frontends werden vom Backend verarbeitet und die passenden Ergebnisse zurückgeliefert.

Die Anwendung wurde nach einer mehrschichtigen Architektur aufgebaut. Dadurch werden die einzelnen Verantwortlichkeiten voneinander getrennt und der Quellcode bleibt übersichtlich und wartbar.

Die Architektur besteht aus den folgenden Schichten:

* Router-Schicht
* Service-Schicht
* Repository-Schicht
* DTO-Schicht

## Verwendete Technologien

### Python

Python dient als Programmiersprache des gesamten Backends. Durch die große Anzahl verfügbarer Bibliotheken und die übersichtliche Syntax eignet sich Python besonders gut für die Entwicklung von Webanwendungen.

### FastAPI

FastAPI bildet die Grundlage des Backends. Das Framework stellt die REST-Endpunkte bereit und verarbeitet eingehende HTTP-Anfragen.

Die Endpunkte werden über sogenannte Router definiert. FastAPI übernimmt dabei die Zuordnung der URL zu der entsprechenden Funktion im Backend.

Beispielsweise wird die URL

```text
GET /rest?email=alpha@acme.de
```

automatisch an die Suchfunktion des Routers weitergeleitet.

Zusätzlich bietet FastAPI eine integrierte Dependency Injection, welche zur Bereitstellung des Repositories und des Services genutzt wird.

### Uvicorn

Die FastAPI-Anwendung wird über den ASGI-Server Uvicorn ausgeführt.

Uvicorn übernimmt dabei:

* Entgegennahme von HTTP-Anfragen
* Weiterleitung an FastAPI
* Rückgabe der HTTP-Antworten

Dadurch kann die Anwendung als Webserver betrieben werden.

### Pydantic

Pydantic wird zur Modellierung und Validierung von Daten eingesetzt.

Für die Datenstrukturen wie Patienten, Adressen oder Rechnungen existieren eigene Modelle. Eingehende Daten können dadurch automatisch geprüft werden.

Beispielsweise wird sichergestellt, dass eine Postleitzahl genau fünf Stellen besitzt oder Felder die erwarteten Datentypen enthalten.

### Loguru

Loguru wird für die Protokollierung von Ereignissen verwendet.

Hierdurch können Suchanfragen, Fehler oder Antwortzeiten während der Entwicklung nachvollzogen werden.

## Schichtenarchitektur

### Router-Schicht

Die Router-Schicht bildet den Einstiegspunkt für alle HTTP-Anfragen.

Beispiele für vorhandene Endpunkte:

```text
GET /rest/{id}
GET /rest?email=...
GET /rest?nachname=...
GET /rest/nachnamen/{teil}
GET /health/liveness
GET /health/readiness
```

Der Router verarbeitet die Anfrage selbst nicht, sondern übergibt sie an die Service-Schicht.

Zusätzlich entscheidet der Router, welches Antwortformat an den Client zurückgegeben wird.

### Service-Schicht

Die Service-Schicht enthält die eigentliche Geschäftslogik.

Ihre Aufgaben sind:

* Verarbeitung der Suchparameter
* Aufruf des Repositories
* Umwandlung der Daten in DTOs
* Behandlung von Fehlerfällen

Findet eine Suche keinen passenden Datensatz, wird eine NotFoundError-Exception ausgelöst. Diese wird anschließend in einen HTTP-Statuscode 404 umgewandelt.

### Repository-Schicht

Für dieses Projekt wird keine Datenbank verwendet.

Stattdessen kommt ein Mock Repository zum Einsatz.

Das Repository enthält mehrere fest hinterlegte Patientendatensätze und simuliert den Zugriff auf eine Datenbank.

Beim Start der Anwendung werden vier Patientenobjekte erzeugt:

* Alpha
* Beta
* Gamma
* Delta

Die Suchfunktionen arbeiten anschließend auf diesen Objekten.

Das Repository unterstützt:

* Suche über ID
* Suche über E-Mail
* Suche über Nachname
* Nachnamen-Vervollständigung
* Pagination

Dadurch kann die komplette Anwendung entwickelt und getestet werden, ohne eine echte Datenbank betreiben zu müssen.

### DTO-Schicht

Zwischen den internen Datenobjekten und den zurückgegebenen Daten werden Data Transfer Objects (DTOs) verwendet.

Dadurch werden nur die tatsächlich benötigten Informationen an das Frontend übertragen.

Zusätzlich wird eine direkte Abhängigkeit zwischen Frontend und den internen Datenstrukturen vermieden.

## Umsetzung der HTML-Ausgabe

Üblicherweise liefern REST-Schnittstellen ihre Daten als JSON zurück.

Für dieses Projekt wurde ein anderer Ansatz gewählt.

Die HTML-Darstellung wird bereits im Backend erzeugt. Das Backend erstellt direkt eine vollständige HTML-Tabelle und sendet diese an das Frontend zurück.

Vereinfacht dargestellt erfolgt die Verarbeitung in folgenden Schritten:

1. Frontend sendet Suchanfrage
2. Router ruft Service auf
3. Service ruft Repository auf
4. Repository liefert Patientendaten
5. Router erzeugt HTML-Code
6. HTML wird direkt an das Frontend zurückgegeben

Beispielsweise wird aus mehreren Patientenobjekten folgende Struktur erzeugt:

```html
<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>Nachname</th>
            <th>E-Mail</th>
        </tr>
    </thead>
    <tbody>
        ...
    </tbody>
</table>
```

Der HTML-Code wird anschließend als HTTP-Response zurückgegeben.

Dadurch muss das Frontend die empfangenen Daten nicht mehr selbst in Tabellen oder Listen umwandeln.

Die Vorteile dieses Ansatzes sind:

* geringerer Implementierungsaufwand im Frontend
* keine zusätzliche Transformation von JSON in HTML
* einfache Darstellung der Suchergebnisse
* schnelle Umsetzung des Projekts

Für die Anforderungen dieses Projekts war dieser Ansatz ausreichend und zweckmäßig.

## Fehlerbehandlung

Für Fehlerfälle werden eigene Exceptions verwendet.

Wird beispielsweise kein passender Patient gefunden, wird eine NotFoundError ausgelöst.

Diese wird anschließend automatisch in einen HTTP-Statuscode 404 umgewandelt.

Dadurch erhält das Frontend eine eindeutige Rückmeldung über fehlende Datensätze.

## Health-Endpunkte

Zusätzlich wurden Health-Endpunkte implementiert.

### Liveness

```text
GET /health/liveness
```

Prüft, ob die Anwendung grundsätzlich erreichbar ist.

### Readiness

```text
GET /health/readiness
```

Prüft, ob die Anwendung betriebsbereit ist.

Diese Endpunkte werden typischerweise für Monitoring oder Verfügbarkeitsprüfungen verwendet.

## Tests

Zur Qualitätssicherung wurden automatisierte Tests mit Pytest umgesetzt.

Die Tests sind in Unit-Tests und Integrationstests unterteilt.

### Unit-Tests

Die Unit-Tests überprüfen einzelne Funktionen der Geschäftslogik unabhängig vom Rest des Systems.

Beispielsweise werden Suchfunktionen des Services isoliert getestet.

### Integrationstests

Die Integrationstests prüfen die vollständige Verarbeitung einer HTTP-Anfrage.

Dabei wird getestet:

* Abruf aller Patienten
* Suche über ID
* Suche über E-Mail
* Suche über Nachname
* Nachnamen-Vervollständigung
* Health-Endpunkte
* Fehlerfälle mit HTTP 404

Hierdurch wird sichergestellt, dass Router, Service und Repository korrekt zusammenarbeiten.

Zum Zeitpunkt der Dokumentation werden insgesamt 46 automatisierte Tests ausgeführt.

## Fazit

Das Backend wurde mit FastAPI auf Basis einer klaren Schichtenarchitektur umgesetzt. Durch die Trennung in Router, Service, Repository und DTOs entsteht eine wartbare Struktur. Die Verwendung eines Mock Repositories ermöglicht die Entwicklung ohne Datenbank. Die direkte Erzeugung von HTML im Backend reduziert den Aufwand im Frontend und vereinfacht die Darstellung der Suchergebnisse. Durch automatisierte Unit- und Integrationstests wird die Funktionsfähigkeit der Anwendung abgesichert.
