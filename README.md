# Voice2Form

## Quick start

```bash
cd voice2form
docker build -t voice2form .
docker run -p 8000:80
```

API endpoints:

| Method | URL | Body |
| ------ | ------------ | -------------------- |
| POST | /stt | audio/wav |
| POST | /parse | use_case, text |
| POST | /speech2json | use_case, audio/wav |

Add new form: edit `app/core/prompts.py` and add to `PROMPTS` dict – **no other code changes**.
