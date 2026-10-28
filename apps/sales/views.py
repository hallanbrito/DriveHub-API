from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.vehicles.repositories import DjangoVehicleRepository
from core.domain.enums import PaymentMethod
from core.domain.exceptions import DomainException
from core.use_cases.sales import (
    ApproveSaleProposalUseCase,
    CompleteSaleUseCase,
    CreateSaleProposalUseCase,
)
from .models import SaleProposalModel
from .permissions import IsManager
from .repositories import DjangoSaleProposalRepository
from .serializers import CreateSaleProposalSerializer, SaleProposalSerializer


class SaleProposalViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SaleProposalSerializer

    def get_queryset(self):
        queryset = SaleProposalModel.objects.select_related("vehicle", "vehicle__brand").all().order_by("-id")
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        return queryset

    @transaction.atomic
    def create(self, request):
        serializer = CreateSaleProposalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            proposal = CreateSaleProposalUseCase(
                DjangoVehicleRepository(), DjangoSaleProposalRepository()
            ).execute(
                vehicle_id=data["vehicle_id"],
                customer_name=data["customer_name"],
                proposed_value=data["proposed_value"],
                payment_method=PaymentMethod(data["payment_method"]),
                down_payment=data["down_payment"],
            )
        except DomainException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        model = SaleProposalModel.objects.select_related("vehicle", "vehicle__brand").get(pk=proposal.id)
        return Response(SaleProposalSerializer(model).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], permission_classes=[IsManager])
    @transaction.atomic
    def approve(self, request, pk=None):
        try:
            proposal = ApproveSaleProposalUseCase(
                DjangoSaleProposalRepository(), DjangoVehicleRepository()
            ).execute(int(pk))
        except DomainException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        model = SaleProposalModel.objects.select_related("vehicle", "vehicle__brand").get(pk=proposal.id)
        return Response(SaleProposalSerializer(model).data)

    @action(detail=True, methods=["post"], permission_classes=[IsManager])
    @transaction.atomic
    def complete(self, request, pk=None):
        try:
            proposal = CompleteSaleUseCase(
                DjangoVehicleRepository(), DjangoSaleProposalRepository()
            ).execute(int(pk))
        except DomainException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        model = SaleProposalModel.objects.select_related("vehicle", "vehicle__brand").get(pk=proposal.id)
        return Response(SaleProposalSerializer(model).data)
