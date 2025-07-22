# Voice2Form

Simple FastAPI service converting speech into structured JSON.

## Requirements

- Python 3.10 or newer (or use Docker)

## Configuration

Endpoints for the external LLM and speech-to-text services are stored in
`config.yml` at the repository root:

```yaml
llm_endpoint: http://llm-container:8080/prediction
stt_endpoint: http://stt-container:5000/stt
```

Adjust these values to match your environment.

## Running with Python

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running with Docker

```bash
docker build -t voice2form .
docker run -p 8000:80 voice2form
```

The API will be available at `http://localhost:8000`.

### API endpoints

| Method | URL | Body |
| ------ | ---------------- | -------------------- |
| POST | /stt | audio/wav |
| POST | /parse | use_case, text |
| POST | /speech2json | use_case, audio/wav |

To add a new form, edit `app/core/prompts.py` and append to the `PROMPTS`
dictionary – **no other code changes are required**.
