def test_create_order_success(client):
    valid_payload = {
        "customer_id": "cust_001",
        "items": [
            {
                "product_id": "prod_100",
                "quantity": 2,
                "unit_price": 150000.0,
            },
            {
                "product_id": "prod_101",
                "quantity": 1,
                "unit_price": 500000.0,
            },
        ],
    }

    response = client.post("/api/orders", json=valid_payload)

    assert response.status_code == 201

    data = response.json()
    assert data["order_id"] == 1
    assert data["status"] == "pending"
    assert data["total"] == 800000.0
    assert data["version"] == 1


def test_create_order_validation_error(client):
    invalid_payload = {
        "items": [
            {
                "product_id": "prod_100",
                "quantity": "hai_cai",
                "unit_price": 150000.0,
            }
        ],
    }

    response = client.post("/api/orders", json=invalid_payload)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_get_order_success(client):
    setup_payload = {
        "customer_id": "cust_002",
        "items": [
            {
                "product_id": "prod_200",
                "quantity": 3,
                "unit_price": 100000.0,
            }
        ],
    }

    create_response = client.post("/api/orders", json=setup_payload)
    assert create_response.status_code == 201

    created_order_id = create_response.json()["order_id"]

    get_response = client.get(f"/api/orders/{created_order_id}")

    assert get_response.status_code == 200

    data = get_response.json()
    assert data["order_id"] == created_order_id
    assert data["total"] == 300000.0
    assert data["status"] == "pending"