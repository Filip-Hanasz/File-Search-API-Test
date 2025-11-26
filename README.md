# File Search API - Gemini Tool

Prosta aplikacja konsolowa do zarządzania bibliotekami embeddingów w Gemini API.

## Dokumentacja

- [Oficjalna dokumentacja - File Search Stores](https://ai.google.dev/api/file-search/file-search-stores?hl=pl)
- [Oficjalna dokumentacja - Documents](https://ai.google.dev/api/file-search/documents?hl=pl)
- [Post wprowadzający - File Search w Gemini API](https://blog.google/technology/developers/file-search-gemini-api/)
- [Przykłady użycia od Google](https://ai.google.dev/gemini-api/docs/file-search?hl=pl)

## Funkcje

1. **Tworzenie nowych bibliotek embeddingów** - Utwórz nową bibliotekę (File Search Store)
2. **Listowanie bibliotek** - Wyświetl wszystkie dostępne biblioteki
3. **Upload plików** - Prześlij pliki do wybranej biblioteki (bezpośrednio do File Search Store)
4. **Listowanie dokumentów** - Wyświetl wszystkie dokumenty w wybranej bibliotece
5. **Kasowanie dokumentów** - Usuń nieaktualne dokumenty z biblioteki
6. **Odpytywanie modelu** - Zadawaj pytania modelowi Gemini z użyciem plików z wybranej biblioteki

## Wymagania

- Python 3.8+
- Klucz API Gemini (GEMINI_API_KEY)

## Instalacja

1. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

2. Utwórz plik `.env` w głównym katalogu projektu i dodaj klucz API:
```bash
GEMINI_API_KEY=twój-klucz-api-tutaj
```

**Uwaga:** Plik `.env` nie powinien być commitowany do repozytorium (dodaj go do `.gitignore`).

## Użycie

Uruchom aplikację:
```bash
python app.py
```

Następnie wybierz opcję z menu:
- `1` - Utwórz nową bibliotekę
- `2` - Listuj biblioteki
- `3` - Upload pliku do biblioteki
- `4` - Listuj dokumenty w bibliotece
- `5` - Usuń dokument z biblioteki
- `6` - Odpytaj model z biblioteką
- `0` - Wyjście

### Przykład użycia opcji 6 (Odpytywanie modelu)

Po wybraniu opcji 6:
1. Wybierz bibliotekę z listy
2. Zadaj pytanie dotyczące plików w bibliotece
3. Model wygeneruje odpowiedź na podstawie zawartości plików
4. Pod odpowiedzią zostaną wyświetlone informacje o użytych plikach/embeddingach

## Uwagi

- Wszystkie dane są przechowywane bezpośrednio w Gemini API
- Aplikacja nie używa lokalnej bazy danych
- Aplikacja używa wyłącznie **File Search API** do zarządzania dokumentami w bibliotekach
- Pliki są automatycznie indeksowane po uploadzie (operacja asynchroniczna)
- Usunięcie dokumentu jest nieodwracalne
- Model używa plików z biblioteki do generowania odpowiedzi - informacje o użytych plikach są wyświetlane pod odpowiedzią

