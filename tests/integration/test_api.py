from decimal import Decimal
from unittest.mock import patch
import pytest
from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.test import APIClient

from apps.sales.models import SaleProposalModel
from apps.vehicles.models import BrandModel, VehicleModel

@pytest.fixture
def auth_users():
    manager_group, _ = Group.objects.get_or_create(name="Manager")
    seller_group, _ = Group.objects.get_or_create(name="Seller")

    manager = User.objects.create_user(username="test_gerente", password="secret_password", is_staff=True)
    manager.groups.add(manager_group)

    seller = User.objects.create_user(username="test_vendedor", password="secret_password", is_staff=False)
    seller.groups.add(seller_group)

    return {"manager": manager, "seller": seller}

@pytest.fixture
def sample_vehicle():
    brand = BrandModel.objects.create(name="Porsche")
    return VehicleModel.objects.create(
        brand=brand,
        model="911 Carrera S",
        factory_year=2023,
        model_year=2024,
        plate="PRC9S11",
        value=Decimal("900000.00"),
        mileage=4000,
        status=VehicleModel.Status.AVAILABLE,
    )

@pytest.mark.django_db
def test_api_vehicle_creation():
    client = APIClient()
    res = client.post(
        "/api/vehicles/vehicles/",
        {
            "brand_name": "Fiat",
            "model": "Pulse",
            "factory_year": 2024,
            "model_year": 2025,
            "value": "100000.00",
            "mileage": 0,
        },
        format="json",
    )
    assert res.status_code == status.HTTP_201_CREATED
    assert VehicleModel.objects.count() == 1
    assert res.data["brand_name"] == "Fiat"

@pytest.mark.django_db
def test_api_vehicle_mileage_update_and_reduction_rejection(sample_vehicle):
    client = APIClient()
    url = f"/api/vehicles/vehicles/{sample_vehicle.id}/mileage/"

    # Sucesso ao aumentar odômetro
    res = client.patch(url, {"mileage": 4500}, format="json")
    assert res.status_code == status.HTTP_200_OK
    assert res.data["mileage"] == 4500

    # Rejeição ao tentar retroceder odômetro
    res_error = client.patch(url, {"mileage": 4200}, format="json")
    assert res_error.status_code == status.HTTP_400_BAD_REQUEST
    assert "não pode ser menor" in res_error.data["detail"]

@pytest.mark.django_db
def test_api_summary_endpoint(sample_vehicle):
    client = APIClient()
    res = client.get("/api/vehicles/vehicles/summary/")
    assert res.status_code == status.HTTP_200_OK
    assert "vehicles" in res.data
    assert "proposals" in res.data
    assert res.data["vehicles"]["available"] >= 1

# Testes de Autenticação e Autorização por Perfil (RBAC)
@pytest.mark.django_db
def test_rbac_approval_anonymous_rejected(sample_vehicle):
    client = APIClient()
    # Criar proposta que exige aprovação
    prop_res = client.post(
        "/api/sales/proposals/",
        {
            "vehicle_id": sample_vehicle.id,
            "customer_name": "Carlos Silva",
            "proposed_value": "820000.00",  # ~9% de desconto -> PENDING_MANAGER
            "payment_method": "CASH",
            "down_payment": "0.00",
        },
        format="json",
    )
    assert prop_res.status_code == status.HTTP_201_CREATED
    proposal_id = prop_res.data["id"]

    # Tentativa anônima de aprovação
    approve_url = f"/api/sales/proposals/{proposal_id}/approve/"
    res_anon = client.post(approve_url)
    assert res_anon.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

@pytest.mark.django_db
def test_rbac_approval_seller_rejected(sample_vehicle, auth_users):
    client = APIClient()
    prop_res = client.post(
        "/api/sales/proposals/",
        {
            "vehicle_id": sample_vehicle.id,
            "customer_name": "Carlos Silva",
            "proposed_value": "820000.00",
            "payment_method": "CASH",
            "down_payment": "0.00",
        },
        format="json",
    )
    proposal_id = prop_res.data["id"]

    # Vendedor autenticado tenta aprovar (deve ser 403 Forbidden)
    client.force_authenticate(user=auth_users["seller"])
    approve_url = f"/api/sales/proposals/{proposal_id}/approve/"
    res_seller = client.post(approve_url)
    assert res_seller.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_rbac_approval_and_complete_manager_authorized(sample_vehicle, auth_users):
    client = APIClient()
    prop_res = client.post(
        "/api/sales/proposals/",
        {
            "vehicle_id": sample_vehicle.id,
            "customer_name": "Carlos Silva",
            "proposed_value": "820000.00",
            "payment_method": "CASH",
            "down_payment": "0.00",
        },
        format="json",
    )
    proposal_id = prop_res.data["id"]

    # Gerente aprova com sucesso
    client.force_authenticate(user=auth_users["manager"])
    approve_url = f"/api/sales/proposals/{proposal_id}/approve/"
    res_manager = client.post(approve_url)
    assert res_manager.status_code == status.HTTP_200_OK
    assert res_manager.data["status"] == "APPROVED"

    # Gerente conclui venda com sucesso
    complete_url = f"/api/sales/proposals/{proposal_id}/complete/"
    res_complete = client.post(complete_url)
    assert res_complete.status_code == status.HTTP_200_OK
    assert res_complete.data["status"] == "COMPLETED"

    # Veículo baixado no estoque
    sample_vehicle.refresh_from_db()
    assert sample_vehicle.status == VehicleModel.Status.SOLD

# Concorrência e Conflito de Estados
@pytest.mark.django_db
def test_concurrency_conflict_when_vehicle_already_reserved(sample_vehicle):
    client = APIClient()
    # Cliente 1 reserva o veículo
    res1 = client.post(
        "/api/sales/proposals/",
        {
            "vehicle_id": sample_vehicle.id,
            "customer_name": "Cliente 1",
            "proposed_value": "880000.00",
            "payment_method": "CASH",
            "down_payment": "0.00",
        },
        format="json",
    )
    assert res1.status_code == status.HTTP_201_CREATED

    # Cliente 2 tenta reservar o mesmo veículo
    res2 = client.post(
        "/api/sales/proposals/",
        {
            "vehicle_id": sample_vehicle.id,
            "customer_name": "Cliente 2",
            "proposed_value": "880000.00",
            "payment_method": "CASH",
            "down_payment": "0.00",
        },
        format="json",
    )
    assert res2.status_code == status.HTTP_400_BAD_REQUEST
    assert "disponível ou reservado ao mesmo cliente" in res2.data["detail"]

# Atomicidade e Rollback Transacional
@pytest.mark.django_db
def test_atomic_rollback_on_failure(sample_vehicle):
    client = APIClient()
    initial_status = sample_vehicle.status
    initial_customer = sample_vehicle.reservation_customer

    # Simular falha durante o salvamento da proposta após o veículo ter sido reservado
    with patch("apps.sales.repositories.DjangoSaleProposalRepository.save", side_effect=RuntimeError("Erro forçado na gravação")):
        with pytest.raises(RuntimeError):
            client.post(
                "/api/sales/proposals/",
                {
                    "vehicle_id": sample_vehicle.id,
                    "customer_name": "Cliente Teste",
                    "proposed_value": "880000.00",
                    "payment_method": "CASH",
                    "down_payment": "0.00",
                },
                format="json",
            )

    # O rollback transacional deve garantir que o veículo NÃO permaneça reservado
    sample_vehicle.refresh_from_db()
    assert sample_vehicle.status == initial_status
    assert sample_vehicle.reservation_customer == initial_customer
    assert SaleProposalModel.objects.count() == 0
