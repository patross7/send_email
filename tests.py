import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_send_email_success(client):
    # Send a POST request with an email address
    data = {"email": "test@example.com", "topic": "topic"}
    response = client.post("/send_email", data=data)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    # Check if the response message is correct
    assert response.data.decode() == "Email sent successfully to " + data['email']

def test_send_email_missing_email(client):
    # Send a POST request without an email address
    response = client.post("/send_email", data={"topic": "topic"})
    
    # Check if the response status code is 500 (Internal Server Error)
    assert response.status_code == 500
