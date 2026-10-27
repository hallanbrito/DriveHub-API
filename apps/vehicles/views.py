from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core.domain.exceptions import DomainException
from core.use_cases.vehicles import CreateVehicleUseCase, UpdateVehicleMileageUseCase
from .models import VehicleModel
from .repositories import DjangoBrandRepository, DjangoVehicleRepository
from .serializers import CreateVehicleSerializer, MileageSerializer, VehicleSerializer

class VehicleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VehicleModel.objects.select_related("brand").all()
    serializer_class = VehicleSerializer
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
    def mileage(self, request, pk=None):
        serializer = MileageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            vehicle = UpdateVehicleMileageUseCase(DjangoVehicleRepository()).execute(int(pk), serializer.validated_data["mileage"])
        except DomainException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        model = VehicleModel.objects.select_related("brand").get(pk=vehicle.id)
        return Response(VehicleSerializer(model).data)
