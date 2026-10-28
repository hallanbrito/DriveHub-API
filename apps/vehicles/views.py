from decimal import Decimal
from django.db import transaction
from django.db.models import Q, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.sales.models import SaleProposalModel
from core.domain.exceptions import DomainException
from core.use_cases.vehicles import CreateVehicleUseCase, UpdateVehicleMileageUseCase
from .models import VehicleModel
from .repositories import DjangoBrandRepository, DjangoVehicleRepository
from .serializers import CreateVehicleSerializer, MileageSerializer, VehicleSerializer


class VehicleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        queryset = VehicleModel.objects.select_related("brand").all().order_by("-id")
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(model__icontains=search) |
                Q(brand__name__icontains=search) |
                Q(plate__icontains=search)
            )
        return queryset

    @transaction.atomic
    def create(self, request):
        serializer = CreateVehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            vehicle = CreateVehicleUseCase(DjangoBrandRepository(), DjangoVehicleRepository()).execute(**serializer.validated_data)
        except DomainException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        model = VehicleModel.objects.select_related("brand").get(pk=vehicle.id)
        return Response(VehicleSerializer(model).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="mileage")
    @transaction.atomic
    def mileage(self, request, pk=None):
        serializer = MileageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            vehicle = UpdateVehicleMileageUseCase(DjangoVehicleRepository()).execute(int(pk), serializer.validated_data["mileage"])
        except DomainException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        model = VehicleModel.objects.select_related("brand").get(pk=vehicle.id)
        return Response(VehicleSerializer(model).data)

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        all_vehicles = VehicleModel.objects.all()
        available_vehicles = all_vehicles.filter(status=VehicleModel.Status.AVAILABLE)
        total_inventory_value = available_vehicles.aggregate(total=Sum("value"))["total"] or Decimal("0.00")

        all_proposals = SaleProposalModel.objects.all()
        completed_proposals = all_proposals.filter(status=SaleProposalModel.Status.COMPLETED)
        total_sales_revenue = completed_proposals.aggregate(total=Sum("proposed_value"))["total"] or Decimal("0.00")

        return Response({
            "vehicles": {
                "total": all_vehicles.count(),
                "available": available_vehicles.count(),
                "reserved": all_vehicles.filter(status=VehicleModel.Status.RESERVED).count(),
                "maintenance": all_vehicles.filter(status=VehicleModel.Status.MAINTENANCE).count(),
                "sold": all_vehicles.filter(status=VehicleModel.Status.SOLD).count(),
                "total_inventory_value": str(total_inventory_value),
            },
            "proposals": {
                "total": all_proposals.count(),
                "approved": all_proposals.filter(status=SaleProposalModel.Status.APPROVED).count(),
                "pending_manager": all_proposals.filter(status=SaleProposalModel.Status.PENDING_MANAGER).count(),
                "completed": completed_proposals.count(),
                "total_sales_revenue": str(total_sales_revenue),
            }
        })
