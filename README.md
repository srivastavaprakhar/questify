# Questify

> A small Retrieval-Augmented Generation (RAG) assistant for university data. Questify builds a FAISS index from a local SQLite database, embeds content with an E5-based embedding model, and answers user questions via a Google Gemini LLM (or other configured model) through a CLI or a FastAPI wrapper.

## Key features
- CLI chat assistant (interactive): `main.py`
- FastAPI HTTP wrapper for programmatic access: `api_wrapper.py`
- Builds a FAISS vector index from the local SQLite database: `embed_and_index.py` + `sqlite_loader.py`
- Simple username/password auth persisted in `database/trial1.db`: `auth/user_auth.py`
- Several helper scripts to seed the DB (departments, faculty, events, playlists)

## Repo layout (important files)
- `main.py` — CLI entrypoint, user login/signup, loads model and index, handles interactive Q&A.
- `api_wrapper.py` — FastAPI app exposing `/signup`, `/login`, `/ask`, and `/health`.
- `gemini_engine.py` — Thin wrapper around Google Generative AI (Gemini) used as the LLM.
- `embed_and_index.py` — Builds and loads the index. Uses an in-repo `E5SmallV2Embedding` (transformers) and Llama-Index vector store (FAISS).
- `sqlite_loader.py` — Turns each DB row into a Document with light FK join summaries for context.
- `auth/user_auth.py` — Simple SQLite-based auth (SHA256 hashed passwords).
- `config.py` — Paths and environment config (DB_PATH, INDEX_PATH, MODEL_PATH, keys).
- `requirements.txt` — Python dependencies used by the project.
- `database/` — Additional modules and/or seeded DB; primary DB file used is `database/trial1.db`.
- `faiss_index/` — Default index persistence directory (created by `embed_and_index`).
- `logs/` — Log files created at runtime (`system.log`, `llama.log`, `retrieval_debug.log`).

## Requirements
- Python 3.10+ recommended
- Install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment variables
- Create a `.env` file in the project root (or set env vars directly).
- Important variables:
  - `GEMINI_API_KEY` — required for `GeminiEngine` (used by `gemini_engine.py`).
  - `SHIVAAY_API_KEY` — optional (present in `config.py`).

## Database & seeding
- The app expects a SQLite DB at `database/trial1.db` by default (see `config.py`).
- Several scripts in the repo insert seed data (run them once to populate the DB):
  - `cse.py`, `department_faculty.py`, `events_academic_events.py`, `subjects_playlist.py` (root-level files) — these create tables and insert rows into `trial1.db`.
  - Alternatively, running the CLI (`python main.py`) or the API will call `init_user_table()` and create the `users` table automatically.

Example (seed DB):

```bash
# run each script once to populate tables (they write to trial1.db)
python cse.py
python department_faculty.py
python events_academic_events.py
python subjects_playlist.py
```

## Build or load the index
- To build the FAISS index from the SQLite DB (this is done automatically by the CLI and API on startup):

```bash
# from Python REPL or script
python -c "from embed_and_index import build_index; build_index()"

# or let main.py/api_wrapper.py build it when starting
```

- Index persistence path is `faiss_index` by default (see `config.py` `INDEX_PATH`).

## Run the CLI assistant

```bash
python main.py
```

The CLI will ask you to login or signup, then build/load the index and allow free-form questions. Type `exit` to quit.

## Run the API server

```bash
# start FastAPI server
uvicorn api_wrapper:app --reload --host 127.0.0.1 --port 8000
```

- Endpoints (basic):
  - `GET /health` — health check
  - `POST /signup` — body: `{ "username": "...", "password": "..." }`
  - `POST /login` — body: `{ "username": "...", "password": "..." }`
  - `POST /ask` — body: `{ "question": "..." }` returns `{ "answer": "..." }`

## Notes & troubleshooting
- The repository uses `transformers` to load `intfloat/e5-small-v2` for embeddings on CPU. Downloading and running the model may be memory/CPU intensive.
- If embedding downloads fail, ensure `transformers` and `torch` are installed and the environment has internet access.
- The LLM implementation in `gemini_engine.py` requires a working Google GenAI key and the `google-genai` package; set `GEMINI_API_KEY` in `.env`.
- Index rebuild: if you modify the database, re-run `build_index()` to regenerate the FAISS index.
- Logs (runtime and retrieval debug) are written to `logs/`.

## Developer notes
- The retrieval pipeline:
  1. `sqlite_loader.get_sqlite_db()` turns DB rows into Documents with `metadata.table`.
  2. `embed_and_index.build_index()` chunks text (SentenceSplitter) and creates embeddings via `E5SmallV2Embedding`.
  3. FAISS vector store is persisted to `faiss_index`.
  4. `main.answer_question()` performs retrieval, writes retrieval traces to `logs/retrieval_debug.log`, infers the most relevant source table, and composes a prompt for the LLM.
- Authentication is intentionally simple (SHA256 hashed passwords in SQLite). For production, use a hardened auth solution.

## Where to start
1. Create and activate a venv, install `requirements.txt`.
2. Add `GEMINI_API_KEY` to `.env`.
3. Seed the database by running the seeding scripts (or use your own DB at `database/trial1.db`).
4. Build the index (or start `main.py`/`api_wrapper.py` which will build it automatically).

If you'd like, I can:
- add a `.env.example` file,
- add a simple shell script to automate setup and seeding, or
- update `requirements.txt` to pin working versions.

---
Generated by a repo scan; adjust the README content to add project-specific details or usage examples you prefer.
