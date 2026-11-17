from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("1. Testing GET / (Frontend Delivery)...")
resp = client.get("/")
assert resp.status_code == 200
assert "InsightAgent" in resp.text
print("   -> Frontend HTML successfully delivered!")

print("2. Testing GET /api/health...")
resp = client.get("/api/health")
assert resp.status_code == 200
print("   -> API health ok:", resp.json())

print("3. Testing GET /api/dataset/summary...")
resp = client.get("/api/dataset/summary")
assert resp.status_code == 200
data = resp.json()
assert data["row_count"] == 9994
print(f"   -> Summary verified: {data['row_count']} rows, {data['column_count']} columns, KPIs: {data['quick_kpis']}")

print("4. Testing GET /api/insights/auto-audit...")
resp = client.get("/api/insights/auto-audit")
assert resp.status_code == 200
audit = resp.json()
print(f"   -> Auto-audit ok: Health score {audit['health_score']}/100, Anomalies: {len(audit['anomalies'])}")

print("5. Testing POST /api/chat (Autonomous AI Data Analyst Query)...")
payload = {
    "message": "Analyze profit margin erosion by discount band and find the destruction point",
    "dataset_id": "default"
}
resp = client.post("/api/chat", json=payload)
assert resp.status_code == 200
chat_resp = resp.json()
print("   -> Agent Answer Preview:", chat_resp["answer"][:100], "...")
print("   -> Execution Steps:", len(chat_resp["execution_steps"]))
print("   -> Chart Type:", chat_resp["chart"]["chart_type"] if chat_resp.get("chart") else "None")
print("   -> Metrics:", chat_resp["metrics"])

print("\n==============================================")
print("ALL SYSTEM VERIFICATION TESTS PASSED (100% OK)!")
print("==============================================")
