# Week 2 – Action Item Extractor

This project is a small FastAPI + SQLite application that lets users paste meeting notes, extract action items, save notes, and mark extracted tasks as done.

## Features

- Heuristic action-item extraction using the starter logic
- LLM-assisted extraction via Ollama using a structured JSON response
- Saving notes into SQLite
- Listing saved notes
- Tracking action items and toggling them as complete
- A minimal frontend for manual testing

## Project Structure

- `app/main.py` – FastAPI app entry point
- `app/db.py` – SQLite connection and data access helpers
- `app/routers/action_items.py` – endpoints for extraction and done-state updates
- `app/routers/notes.py` – endpoints for note creation and listing
- `app/services/extract.py` – heuristic and LLM extraction logic
- `frontend/index.html` – small browser UI
- `tests/test_extract.py` – unit tests for the extractor

## Setup

1. Activate the environment:
   ```bash
   conda activate cs146s
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Make sure Ollama is available locally and that a model such as `llama3.1:8b` has been pulled:
   ```bash
   ollama pull llama3.1:8b
   ```
4. Start the application:
   ```bash
   poetry run uvicorn week2.app.main:app --reload
   ```
5. Open the app at `http://127.0.0.1:8000/`.

## API Endpoints

- `POST /action-items/extract` – extracts action items with the heuristic parser
- `POST /action-items/extract-llm` – extracts action items through Ollama
- `GET /action-items` – lists action items
- `POST /action-items/{id}/done` – marks an action item as completed
- `POST /notes` – creates a note
- `GET /notes` – lists all notes
- `GET /notes/{note_id}` – retrieves a single note

## Running Tests

```bash
python -m pytest week2/tests/test_extract.py
```
