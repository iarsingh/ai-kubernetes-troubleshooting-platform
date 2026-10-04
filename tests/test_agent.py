from fastapi.testclient import TestClient
from k8sai.main import app

client = TestClient(app)


def test_runs_and_refuses_a_write():
    payload = client.post("/agent/run", json={"goal": 'troubleshoot the deploy', **{'payload': {'events': ['Failed to pull image']}}}).json()
    assert payload["refused"] is False
    assert payload["applied"] is False
    assert payload["hypothesis"] == "image_pull"
    refused = client.post("/agent/run", json={"goal": 'apply the old manifest'}).json()
    assert refused["refused"] is True
