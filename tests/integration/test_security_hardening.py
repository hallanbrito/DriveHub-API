import importlib
import os
from decimal import Decimal
from unittest.mock import patch
import pytest
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.vehicles.models import BrandModel, VehicleModel

# -------------------------------------------------------------
# P0 — Testes de Seed Seguro e Proteção de Ambiente
# -------------------------------------------------------------

@pytest.mark.django_db
def test_seed_drivehub_blocked_in_production():
    """Garante que o comando seed_drivehub recuse execução em ambiente de produção."""
    with patch.object(settings, "IS_PRODUCTION", True):
        with pytest.raises(CommandError, match="estritamente proibido em ambiente de produção"):
            call_command("seed_drivehub")

@pytest.mark.django_db
def test_seed_drivehub_does_not_delete_existing_data_without_reset():
    """Garante que por padrão o comando não apaga dados existentes."""
    brand = BrandModel.objects.create(name="Marca Teste")
    veh = VehicleModel.objects.create(
        brand=brand,
        model="Modelo Teste",
        factory_year=2024,
        model_year=2024,
        value=Decimal("100000.00"),
        mileage=100,
    )
    initial_count = VehicleModel.objects.count()

    # Executa seed sem a flag --reset
    call_command("seed_drivehub")

    # Os dados anteriores permanecem inalterados
    assert VehicleModel.objects.count() == initial_count
    assert VehicleModel.objects.filter(pk=veh.pk).exists()

@pytest.mark.django_db
def test_seed_drivehub_resets_only_when_explicitly_requested():
    """Garante que a limpeza só ocorre quando --reset é explicitamente passado."""
    brand = BrandModel.objects.create(name="Marca Antiga")
    VehicleModel.objects.create(
        brand=brand,
        model="Modelo Antigo",
        factory_year=2020,
        model_year=2020,
        value=Decimal("50000.00"),
        mileage=50000,
    )

    # Executa com --reset explícito
    call_command("seed_drivehub", reset=True, manager_password="pass_gerente_123", seller_password="pass_vendedor_123")

    # Os veículos de demonstração padrão foram criados
    assert VehicleModel.objects.filter(model="911 Carrera S").exists()
    assert not VehicleModel.objects.filter(model="Modelo Antigo").exists()

@pytest.mark.django_db
def test_seed_drivehub_generates_safe_random_passwords_without_hardcoded_defaults():
    """Garante que as senhas não sejam fixas e que sejam geradas de forma segura."""
    # Executa sem flags de senha
    call_command("seed_drivehub", reset=True)

    gerente = User.objects.get(username="gerente")
    vendedor = User.objects.get(username="vendedor")

    # As senhas antigas previsíveis NÃO devem autenticar
    assert authenticate(username="gerente", password="gerente123") is None
    assert authenticate(username="vendedor", password="vendedor123") is None
    assert gerente.is_staff is True
    assert vendedor.is_staff is False

# -------------------------------------------------------------
# P1 — Testes de Validação de Configurações de Produção
# -------------------------------------------------------------

def test_production_settings_reject_debug_true():
    """Garante que o carregamento das configurações de produção rejeite DEBUG=True."""
    env_vars = {
        "DJANGO_ENV": "production",
        "DEBUG": "True",
        "SECRET_KEY": "uma-chave-longa-e-segura-com-mais-de-32-caracteres",
        "ALLOWED_HOSTS": "api.drivehub.com.br",
        "CORS_ALLOWED_ORIGINS": "https://drivehub.com.br",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        with pytest.raises(ValueError, match="DEBUG=True é estritamente proibido"):
            # Recarrega módulo de settings para disparar validação pré-inicialização
            import app.settings
            importlib.reload(app.settings)

def test_production_settings_reject_insecure_secret_key():
    """Garante que o carregamento de produção rejeite chaves fracas ou de desenvolvimento."""
    env_vars = {
        "DJANGO_ENV": "production",
        "DEBUG": "False",
        "SECRET_KEY": "django-insecure-chave-fraca",
        "ALLOWED_HOSTS": "api.drivehub.com.br",
        "CORS_ALLOWED_ORIGINS": "https://drivehub.com.br",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        with pytest.raises(ValueError, match="não pode ser a chave de desenvolvimento"):
            import app.settings
            importlib.reload(app.settings)

def test_production_settings_reject_wildcard_allowed_hosts():
    """Garante que o carregamento de produção rejeite wildcard em ALLOWED_HOSTS."""
    env_vars = {
        "DJANGO_ENV": "production",
        "DEBUG": "False",
        "SECRET_KEY": "uma-chave-longa-e-segura-com-mais-de-32-caracteres",
        "ALLOWED_HOSTS": "*",
        "CORS_ALLOWED_ORIGINS": "https://drivehub.com.br",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        with pytest.raises(ValueError, match="sem curingas"):
            import app.settings
            importlib.reload(app.settings)

def test_production_settings_reject_wildcard_cors():
    """Garante que o carregamento de produção rejeite wildcard em CORS_ALLOWED_ORIGINS."""
    env_vars = {
        "DJANGO_ENV": "production",
        "DEBUG": "False",
        "SECRET_KEY": "uma-chave-longa-e-segura-com-mais-de-32-caracteres",
        "ALLOWED_HOSTS": "api.drivehub.com.br",
        "CORS_ALLOWED_ORIGINS": "*",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        with pytest.raises(ValueError, match="sem curinga"):
            import app.settings
            importlib.reload(app.settings)

# Garante a restauração do settings normal de desenvolvimento após testes de reload
@pytest.fixture(autouse=True)
def restore_dev_settings():
    yield
    dev_env = {
        "DJANGO_ENV": "development",
        "DEBUG": "True",
    }
    with patch.dict(os.environ, dev_env, clear=False):
        import app.settings
        importlib.reload(app.settings)
