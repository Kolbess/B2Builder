# Specyfikacja Techniczna: B2Builder

## 1. Wstęp i Cel Projektu
B2Builder to specjalistyczne API typu SaaS przeznaczone dla sektora B2B [cite: 3]. Głównym celem systemu jest automatyzacja procesu generowania dokumentów PDF na podstawie danych JSON [cite: 4]. Rozwiązuje to problem kosztownego budowania własnych silników renderujących w systemach CRM/ERP [cite: 5].

---

## 2. Opis Funkcjonalności

### 2.1. Punkty Końcowe API (Endpoints)
* **POST /v1/generate**: Główny punkt dostępowy systemu [cite: 12]. Przyjmuje identyfikator szablonu oraz obiekt danych JSON, zwracając gotowy plik PDF w formie strumienia binarnego [cite: 12].
* **GET /v1/templates**: Zwraca listę wszystkich dostępnych wzorów dokumentów, takich jak standardowe faktury czy certyfikaty [cite: 13].
* **GET /docs**: Interaktywna dokumentacja Swagger UI, pozwalająca na testowanie endpointów "na żywo" [cite: 14].

### 2.2. System Szablonów
System opiera się na separacji warstwy danych od prezentacji [cite: 16]. Szablony budowane w HTML/CSS pozwalają na:
* Stosowanie niestandardowych, nowoczesnych czcionek bezszeryfowych [cite: 17].
* Dodawanie logotypów firmowych zakodowanych w formacie Base64 [cite: 18].
* Renderowanie dynamicznych tabel (np. list produktów na fakturach) [cite: 19].

---

## 3. Wygląd i Estetyka dokumentów
Zgodnie z wytycznymi B2Builder, dokumenty muszą cechować się:
* **Czystym układem**: Minimalistyczny design z dużym marginesem.
* **Typografią**: Wykorzystanie nowoczesnych fontów (np. Roboto, Open Sans).
* **Akcentami**: Kolorystyka marki w nagłówkach i tabelach.

---

## 4. Wymagania Techniczne

| Komponent | Technologia | Rola |
| :--- | :--- | :--- |
| **Język** | Python 3.10+ | Podstawa logiczna aplikacji [cite: 9]. |
| **Framework** | FastAPI | Obsługa asynchronicznych zapytań HTTP i OpenAPI [cite: 9]. |
| **Szablony** | Jinja2 | Dynamiczne wstrzykiwanie danych do HTML [cite: 9]. |
| **Silnik PDF** | WeasyPrint | Renderowanie HTML/CSS do formatu PDF [cite: 10]. |
| **Walidacja** | Pydantic | Rygorystyczna kontrola typów danych wejściowych [cite: 9]. |
| **Serwer** | Uvicorn | Serwer ASGI do obsługi ruchu [cite: 9]. |

---

## 5. Bezpieczeństwo i Struktura Danych

### Autoryzacja
* Dostęp chroniony za pomocą **X-API-KEY** przesyłanego w nagłówku zapytania [cite: 21].
* Błędy autoryzacji zwracają czytelny kod **HTTP 401**.

### Walidacja Danych
Każde żądanie przechodzi walidację schematu przed procesem renderowania [cite: 22]. Błędne dane JSON (np. brak wymaganych pól) skutkują błędem **HTTP 422** [cite: 22].

### Przykładowy Model Pydantic (Logic)
```python
from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    template_id: str = Field(..., description="ID szablonu, np. 'invoice_standard'")
    data: dict = Field(..., description="Dane JSON pasujące do schematu wybranego szablonu")
```
