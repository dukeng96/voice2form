from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_parse_endpoint(monkeypatch):
    def fake_parse_record(use_case: str, text: str):
        return {"ok": True}
    monkeypatch.setattr("app.api.routes.parse_record", fake_parse_record)
    resp = client.post("/parse", data={"use_case": "vat_tu", "text": "abc"})
    assert resp.status_code == 200
    assert resp.json() == {"data": {"ok": True}}
