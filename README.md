# Green Agri Voice Backend

## Quick start

```bash
git clone …
cd agri_voice_backend
docker build -t agri-ai .
docker run -p 8000:80 --env-file .env agri-ai
```

API endpoints:

| Method | URL | Body |
| ------ | ------------ | -------------------- |
| POST | /stt | audio/wav |
| POST | /parse | use_case, text |
| POST | /speech2json | use_case, audio/wav |

Add new form: edit `app/core/prompts.py` and add to `PROMPTS` dict – **no other code changes**.
