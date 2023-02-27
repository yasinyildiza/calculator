def test_status(test_client):
    response = test_client.get("/status")
    assert response.status_code == 200
