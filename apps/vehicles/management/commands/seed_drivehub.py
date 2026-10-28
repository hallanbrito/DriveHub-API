import os
import secrets
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand, CommandError

from apps.sales.models import SaleProposalModel
from apps.sales.repositories import DjangoSaleProposalRepository
from apps.vehicles.models import BrandModel, VehicleModel
from apps.vehicles.repositories import DjangoBrandRepository, DjangoVehicleRepository
from core.domain.enums import PaymentMethod
from core.use_cases.sales import ApproveSaleProposalUseCase, CompleteSaleUseCase, CreateSaleProposalUseCase
from core.use_cases.vehicles import CreateVehicleUseCase


class Command(BaseCommand):
    help = "Popula o showroom com veículos e propostas para demonstração (exclusivo para desenvolvimento)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Limpa explicitamente propostas e veículos existentes antes de popular (restrito a desenvolvimento).",
        )
        parser.add_argument(
            "--manager-password",
            type=str,
            default=None,
            help="Define a senha para o usuário gerente (se omitido, gera uma senha aleatória segura).",
        )
        parser.add_argument(
            "--seller-password",
            type=str,
            default=None,
            help="Define a senha para o usuário vendedor (se omitido, gera uma senha aleatória segura).",
        )

    def handle(self, *args, **options):
        # Proteção P0: Bloqueio absoluto em produção
        if getattr(settings, "IS_PRODUCTION", False):
            raise CommandError("O comando seed_drivehub é estritamente proibido em ambiente de produção.")

        should_reset = options["reset"]

        # Proteção P0: Não apagar dados por padrão
        if not should_reset and VehicleModel.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "O banco de dados já possui veículos cadastrados. Nenhuma alteração foi realizada.\n"
                    "Para resetar e repopular os dados em ambiente local, execute novamente com a flag explícita: --reset"
                )
            )
            return

        if should_reset:
            self.stdout.write(self.style.WARNING("Reset explícito solicitado: limpando propostas e veículos..."))
            SaleProposalModel.objects.all().delete()
            VehicleModel.objects.all().delete()
            BrandModel.objects.all().delete()

        # Proteção P0: Remoção de senhas fixas e geração segura
        manager_password = (
            options["manager_password"]
            or os.environ.get("SEED_MANAGER_PASSWORD")
            or secrets.token_urlsafe(16)
        )
        seller_password = (
            options["seller_password"]
            or os.environ.get("SEED_SELLER_PASSWORD")
            or secrets.token_urlsafe(16)
        )

        self.stdout.write(self.style.MIGRATE_HEADING("Configurando grupos e operadores de desenvolvimento..."))
        manager_group, _ = Group.objects.get_or_create(name="Manager")
        seller_group, _ = Group.objects.get_or_create(name="Seller")

        # Gerente
        gerente, _ = User.objects.get_or_create(
            username="gerente",
            defaults={"email": "gerente@drivehub.local", "is_staff": True},
        )
        gerente.set_password(manager_password)
        gerente.is_staff = True
        gerente.groups.add(manager_group)
        gerente.save()

        # Vendedor
        vendedor, _ = User.objects.get_or_create(
            username="vendedor",
            defaults={"email": "vendedor@drivehub.local", "is_staff": False},
        )
        vendedor.set_password(seller_password)
        vendedor.is_staff = False
        vendedor.groups.add(seller_group)
        vendedor.save()

        self.stdout.write(f"  + Gerente configurado: 'gerente' | Senha gerada/atribuída: {manager_password}")
        self.stdout.write(f"  + Vendedor configurado: 'vendedor' | Senha gerada/atribuída: {seller_password}")

        brand_repo = DjangoBrandRepository()
        vehicle_repo = DjangoVehicleRepository()
        proposal_repo = DjangoSaleProposalRepository()

        create_vehicle = CreateVehicleUseCase(brand_repo, vehicle_repo)
        create_proposal = CreateSaleProposalUseCase(vehicle_repo, proposal_repo)
        approve_proposal = ApproveSaleProposalUseCase(proposal_repo, vehicle_repo)
        complete_sale = CompleteSaleUseCase(vehicle_repo, proposal_repo)

        self.stdout.write(self.style.MIGRATE_HEADING("Cadastrando veículos do showroom..."))

        vehicles_data = [
            {
                "brand_name": "Porsche",
                "model": "911 Carrera S",
                "factory_year": 2023,
                "model_year": 2024,
                "plate": "PRC9S11",
                "value": Decimal("980000.00"),
                "mileage": 4200,
                "photo_url": "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "brand_name": "BMW",
                "model": "M3 Competition M xDrive",
                "factory_year": 2023,
                "model_year": 2024,
                "plate": "BMW3M03",
                "value": Decimal("815000.00"),
                "mileage": 7800,
                "photo_url": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "brand_name": "Mercedes-Benz",
                "model": "C300 AMG Line",
                "factory_year": 2024,
                "model_year": 2024,
                "plate": "MBZ3C00",
                "value": Decimal("440000.00"),
                "mileage": 1200,
                "photo_url": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "brand_name": "Audi",
                "model": "RS6 Avant Performance",
                "factory_year": 2023,
                "model_year": 2023,
                "plate": "AUD6R60",
                "value": Decimal("1180000.00"),
                "mileage": 11500,
                "photo_url": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "brand_name": "BYD",
                "model": "Seal EV AWD 530cv",
                "factory_year": 2024,
                "model_year": 2025,
                "plate": "BYD5E41",
                "value": Decimal("299800.00"),
                "mileage": 500,
                "photo_url": "https://images.unsplash.com/photo-1590362891991-f776e747a588?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "brand_name": "Toyota",
                "model": "Corolla Cross GR-Sport",
                "factory_year": 2024,
                "model_year": 2024,
                "plate": "TOY4C77",
                "value": Decimal("198900.00"),
                "mileage": 8900,
                "photo_url": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "brand_name": "Volvo",
                "model": "XC60 T8 Recharge Ultimate",
                "factory_year": 2023,
                "model_year": 2024,
                "plate": "VLV6X88",
                "value": Decimal("465000.00"),
                "mileage": 15400,
                "photo_url": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1200&q=80",
            },
        ]

        created_vehicles = []
        for v in vehicles_data:
            veh = create_vehicle.execute(**v)
            created_vehicles.append(veh)
            self.stdout.write(f"  + Veículo criado: {v['brand_name']} {v['model']} ({v['plate']})")

        self.stdout.write(self.style.MIGRATE_HEADING("Gerando propostas comerciais de demonstração..."))

        audi = created_vehicles[3]
        p1 = create_proposal.execute(
            vehicle_id=audi.id,
            customer_name="Dr. Henrique Vasconcelos",
            proposed_value=Decimal("1085000.00"),
            payment_method=PaymentMethod.FINANCED,
            down_payment=Decimal("300000.00"),
        )
        self.stdout.write(f"  + Proposta 1 criada: Audi RS6 -> {p1.customer_name} (Status: {p1.status.value})")

        toyota = created_vehicles[5]
        p2 = create_proposal.execute(
            vehicle_id=toyota.id,
            customer_name="Mariana Silveira",
            proposed_value=Decimal("193000.00"),
            payment_method=PaymentMethod.CASH,
            down_payment=Decimal("0.00"),
        )
        self.stdout.write(f"  + Proposta 2 criada: Corolla Cross -> {p2.customer_name} (Status: {p2.status.value})")

        volvo = created_vehicles[6]
        p3 = create_proposal.execute(
            vehicle_id=volvo.id,
            customer_name="Roberto Albuquerque",
            proposed_value=Decimal("450000.00"),
            payment_method=PaymentMethod.CASH,
            down_payment=Decimal("0.00"),
        )
        if p3.requires_manager_approval:
            approve_proposal.execute(p3.id)
        complete_sale.execute(p3.id)
        self.stdout.write(f"  + Proposta 3 criada e concluída: Volvo XC60 -> {p3.customer_name} (Veículo VENDIDO)")

        self.stdout.write(self.style.SUCCESS("Showroom populado com sucesso!"))
