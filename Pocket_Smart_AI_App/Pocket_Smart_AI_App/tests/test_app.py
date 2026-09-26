from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_home_requires_auth():

    response = client.post(

        "/api/generate-home",

        json={

            "budget": 10000,

            "rooms": [
                "Bedroom"
            ],

            "style": "modern",

            "items": {},

            "priorities": []
        }
    )


    assert response.status_code == 401

