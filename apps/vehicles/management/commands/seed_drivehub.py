from decimal import Decimal
from django.core.management.base import BaseCommand

from apps.sales.models import SaleProposalModel
from apps.sales.repositories import DjangoSaleProposalRepository
from apps.vehicles.models import BrandModel, VehicleModel
from apps.vehicles.repositories import DjangoBrandRepository, DjangoVehicleRepository
from core.domain.enums import PaymentMethod
from core.use_cases.sales import ApproveSaleProposalUseCase, CompleteSaleUseCase, CreateSaleProposalUseCase
from core.use_cases.vehicles import CreateVehicleUseCase


class Command(BaseCommand):
    help = "Popula o banco de dados com veículos e propostas realistas para demonstração"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Limpando dados antigos..."))
        SaleProposalModel.objects.all().delete()
        VehicleModel.objects.all().delete()
        BrandModel.objects.all().delete()

        brand_repo = DjangoBrandRepository()
        vehicle_repo = DjangoVehicleRepository()
        proposal_repo = DjangoSaleProposalRepository()

        create_vehicle = CreateVehicleUseCase(brand_repo, vehicle_repo)
        create_proposal = CreateSaleProposalUseCase(vehicle_repo, proposal_repo)
        approve_proposal = ApproveSaleProposalUseCase(proposal_repo)
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
                "mileage": 14000,
                "photo_url": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "brand_name": "Land Rover",
                "model": "Defender 110 X-Dynamic HSE",
                "factory_year": 2023,
                "model_year": 2023,
                "plate": "LND1D10",
                "value": Decimal("750000.00"),
                "mileage": 16200,
                "photo_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",
            },
        ]

        created_vehicles = []
        for v in vehicles_data:
            veh = create_vehicle.execute(**v)
            created_vehicles.append(veh)
            self.stdout.write(f"  + Veículo criado: {v['brand_name']} {v['model']} ({v['plate']})")

        self.stdout.write(self.style.MIGRATE_HEADING("Gerando propostas comerciais de demonstração..."))

        # Proposta 1: Audi RS6 com desconto de ~8% (requer aprovação gerencial)
        audi = created_vehicles[3]
        p1 = create_proposal.execute(
            vehicle_id=audi.id,
            customer_name="Dr. Henrique Vasconcelos",
            proposed_value=Decimal("1085000.00"),  # ~8% de desconto
            payment_method=PaymentMethod.FINANCED,
            down_payment=Decimal("300000.00"),  # > 20%
        )
        self.stdout.write(f"  + Proposta 1 criada: Audi RS6 -> {p1.customer_name} (Status: {p1.status.value})")

        # Proposta 2: Toyota Corolla Cross com desconto de 3% (aprovada automaticamente)
        toyota = created_vehicles[5]
        p2 = create_proposal.execute(
            vehicle_id=toyota.id,
            customer_name="Mariana Silveira",
            proposed_value=Decimal("193000.00"),
            payment_method=PaymentMethod.CASH,
            down_payment=Decimal("0.00"),
        )
        self.stdout.write(f"  + Proposta 2 criada: Corolla Cross -> {p2.customer_name} (Status: {p2.status.value})")

        # Proposta 3: Volvo XC60 aprovada e concluída (Venda Fechada)
        volvo = created_vehicles[6]
        p3 = create_proposal.execute(
            vehicle_id=volvo.id,
            customer_name="Roberto Albuquerque",
            proposed_value=Decimal("450000.00"),
            payment_method=PaymentMethod.CASH,
            down_payment=Decimal("0.00"),
        )
        # Se tiver precisado de gerente, aprova
        if p3.requires_manager_approval:
            approve_proposal.execute(p3.id)
        # Conclui venda
        complete_sale.execute(p3.id)
        self.stdout.write(f"  + Proposta 3 criada e concluída: Volvo XC60 -> {p3.customer_name} (Veículo VENDIDO)")

        self.stdout.write(self.style.SUCCESS("Showroom populado com sucesso!"))
