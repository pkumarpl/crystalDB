"""Integration tests for API endpoints."""

from fastapi.testclient import TestClient

from crystaldb.models import Material


def test_health_endpoint(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client: TestClient):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_list_materials_empty(client: TestClient):
    """Test listing materials when database is empty."""
    response = client.get("/api/v1/materials")
    assert response.status_code == 200
    assert response.json() == []


def test_create_material(client: TestClient):
    """Test creating a new material."""
    material_data = {
        "compound_name": "Test Material",
        "chemical_formula": "C6H6",
        "canonical_smile": "c1ccccc1",
        "type": "organic",
        "cas_number": "71-43-2",
        "product_number": "TEST123",
        "supplier": "Test Supplier",
    }

    response = client.post("/api/v1/materials", json=material_data)
    assert response.status_code == 201
    data = response.json()
    assert data["compound_name"] == "Test Material"
    assert data["material_id"] is not None


def test_get_material(client: TestClient, sample_material: Material):
    """Test getting a specific material."""
    response = client.get(f"/api/v1/materials/{sample_material.material_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["material_id"] == sample_material.material_id
    assert data["compound_name"] == sample_material.compound_name


def test_get_material_not_found(client: TestClient):
    """Test getting a non-existent material."""
    response = client.get("/api/v1/materials/99999")
    assert response.status_code == 404


def test_update_material(client: TestClient, sample_material: Material):
    """Test updating a material."""
    update_data = {"compound_name": "Updated Compound"}

    response = client.put(
        f"/api/v1/materials/{sample_material.material_id}",
        json=update_data,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["compound_name"] == "Updated Compound"


def test_delete_material(client: TestClient, sample_material: Material):
    """Test deleting a material."""
    response = client.delete(f"/api/v1/materials/{sample_material.material_id}")
    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/api/v1/materials/{sample_material.material_id}")
    assert response.status_code == 404
