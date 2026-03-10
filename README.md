# 📄 B2Builder – Document Generation API

**B2Builder** to nowoczesne API typu SaaS zbudowane w Pythonie (**FastAPI**), które umożliwia błyskawiczną konwersję danych JSON na profesjonalne dokumenty PDF. Rozwiązanie idealne dla systemów ERP, platform e-commerce i aplikacji edukacyjnych wymagających masowego generowania faktur, raportów czy certyfikatów.

---

### ✨ Główne cechy

* **JSON-to-PDF** – Przesyłasz ustrukturyzowane dane, otrzymujesz gotowy dokument w ułamku sekundy.
* **Template System** – Elastyczna obsługa dynamicznych szablonów przy użyciu silnika Jinja2.
* **Automatyczna Dokumentacja** – Pełna specyfikacja OpenAPI (Swagger) dostępna pod adresem `/docs`.
* **SaaS Ready** – Bezpieczeństwo przede wszystkim – wbudowany system autoryzacji kluczami API.
* **Pythonic Design** – Wykorzystanie asynchroniczności FastAPI (`async/await`) dla maksymalnej przepustowości.

---

### 🛠 Stos technologiczny

| Komponent | Technologia |
| :--- | :--- |
| **Core** | Python 3.9+ / FastAPI |
| **PDF Engine** | WeasyPrint |
| **Templating** | Jinja2 |
| **Auth** | API Key Header Authentication |
| **Docs** | Swagger UI / ReDoc |

---

### 🚀 Development setup

1. **Environment variables**
   - Copy `.env.example` to `.env` and fill in your values.
   - At minimum set `API_KEY` to a secret string used by clients via `X-API-KEY` when
     calling *this* B2Builder service (e.g. `POST /generate`, `GET /templates`).
     It isn’t an external API key – it simply authenticates requests made to the
     local/remote instance of the B2Builder API.
   - The `.env` file is already ignored by Git (see `.gitignore`).

> **Note:** only the `POST /generate` endpoint accepts POST requests; a GET
> returns "Method Not Allowed". The response is a PDF file so the Swagger UI will
> prompt you to download it instead of showing raw text. Visiting the root path
> (`/`) will now redirect to `/docs` so you can explore the API interactively.


2. **Run tests locally**
   ```bash
   python -m venv .venv          # create virtual environment
   .\\.venv\\Scripts\\activate   # on Windows
   pip install -r requirements.txt
   pytest                       # run unit tests
   ```
   > The test harness loads `.env` (via python-dotenv) before importing the
   > application. If you set `API_KEY` in `.env`, the same value will be used
   > in `tests/test_auth.py`.

3. **Launching the service**
   - **Docker**: `docker compose up --build` (listens on port 8000). The compose
     file now reads your `.env` automatically via `env_file`, so put your
     `API_KEY` there instead of editing the YAML.
   - **Direct**: `uvicorn app.main:app --reload` for fast development.

4. **Running tests in Docker (clean environment)**
   Instead of relying on your host virtual environment, you can execute the
   same test suite inside the container image:

   ```bash
   # build the image first (or let compose do it automatically)
   # (rebuild if you’ve modified Python code, e.g. added app/__init__.py)
   docker compose build --no-cache

   # run pytest in a one‑off container.
   # Some older "docker compose" versions don’t support `--env-file` on `run`;
   # in that case simply pass the key explicitly (see PowerShell example below),
   # or mount the `.env` file into `/app` so that python-dotenv can read it.
   docker compose run --rm b2builder-api pytest -q
   ```
   ```powershell
   # Windows alternative using PowerShell variable expansion (works regardless of
   # compose version):
   docker compose run --rm b2builder-api pytest -q
   ```
   ```yaml
   # example docker-compose snippet for mounting .env into container
   services:
     b2builder-api:
       volumes:
         - .env:/app/.env:ro
   ```

   The container image already has all dependencies (including pytest).
   `--rm` ensures the test container is discarded after the run.
   You can set additional environment variables as needed.

---

### 📁 Template assets

Templates may include logos or custom fonts by passing an `assets` object in
the payload sent to `POST /generate`:

```json
{
  "template_id": "invoice_standard",
  "data": {
    "title": "Hello",
    "content": "World",
    "assets": {
      "logo": "data:image/png;base64,<base64-data>",
      "fonts": {
        "MyFont": "<base64-ttf-or-woff>"
      }
    }
  }
}
```

* **Logo** should be a data‑URI with image mime type (PNG, JPEG etc.). The
  renderer will inject it into the HTML at `{{ assets.logo }}`.
* **Fonts** must be base64‑encoded font files (TTF/WOFF/etc). They are turned
  into `@font-face` rules automatically so they can be used by name in the
  template CSS.

These assets are purely optional; sending an empty object (`{}`) has no effect.

4. **Additional secrets**
   - Add any other API keys or config values to `.env` and access via
     `os.getenv()` in your code.

> 🔒 **Security tip:** Do not commit real secrets; keep them in `.env` or
> your preferred secrets manager.

