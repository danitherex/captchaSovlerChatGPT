# Automatische Buchung Hochschulsport



## Beschreibung

Dieses Dockerfile ermöglicht eine automatische Anmeldung beim Hochschulsport in Mannheim.

Mit diesem Dockerfile können Sie eine Anwendung erstellen, die automatisch eine Anmeldung beim Hochschulsport in Mannheim durchführt. Die Anwendung basiert auf Docker und verwendet die angegebenen Konfigurationen, um den Anmeldeprozess zu automatisieren.

Verwendung:
- Stellen Sie sicher, dass Docker auf Ihrem System installiert ist.
- Erstellen Sie ein Docker-Image mit diesem Dockerfile.
- Führen Sie das erstellte Docker-Image aus, um die automatische Anmeldung beim Hochschulsport in Mannheim zu starten.

Hinweis: Bitte stellen Sie sicher, dass Sie über die erforderlichen Anmeldeinformationen verfügen und die rechtlichen Bestimmungen einhalten, bevor Sie diese Anwendung verwenden.


## Installation

1. Klone das Repository.
2. Kopiere die Datei `.env.example` und benenne sie in `.env` um.
3. Fülle die erforderlichen Umgebungsvariablen in der `.env` Datei aus.

## Verwendung

1. Führe das Docker-Image mit folgendem Befehl aus:
`docker run --env-file .env danitherex/buchungSport`
