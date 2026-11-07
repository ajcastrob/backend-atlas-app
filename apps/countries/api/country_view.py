from rest_framework import status
from rest_framework.views import Response
from rest_framework import viewsets
from apps.countries.api.country_serialazer import CountrySerializer
from apps.countries.models import Country


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.filter(state=True)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return (
            self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        )

    # GET
    def list(self, request):
        countries_serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(countries_serializer.data, status=status.HTTP_200_OK)

    # POST
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "País añadido correctamente",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "message": "Hubo error al añadir un país",
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # DELETE
    def destroy(self, request, pk=None):
        country = self.get_queryset().filter(id=pk).first()
        if country:
            country.soft_delete()
            return Response(
                {"message": "País eliminado de forma correcta"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"message": "El país no existe"},
            status=status.HTTP_400_BAD_REQUEST,
        )
